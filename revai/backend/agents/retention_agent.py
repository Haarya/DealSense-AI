import os
import json
import logging
from typing import TypedDict, Annotated, List, Optional
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from sqlalchemy.future import select
from pydantic import BaseModel, Field

from database import AsyncSessionLocal
from models.account import Account
from models.agent_log import AgentLog
from services.retention_service import compute_retention_risk

logger = logging.getLogger(__name__)

class RetentionState(TypedDict):
    account_id: str
    org_id: str
    
    # State loaded from DB
    company_name: str
    usage_data: dict
    
    # State updated by nodes
    churn_score: int
    churn_reason_system: str
    churn_reason_ai: str
    intervention: str
    email_draft: str

class ChurnReasonResult(BaseModel):
    reason: str = Field(description="A concise 1-sentence explanation of the primary churn risk based on the signals.")

class InterventionResult(BaseModel):
    email_draft: str = Field(description="The body of the outreach email to the customer")
    recommendation: str = Field(description="Internal recommendation for next steps")

# ---------------------------------------------
# NODES
# ---------------------------------------------
async def gather_signals(state: RetentionState):
    """
    Node 1 -- gather_signals
    Pull usage_data from DB.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Account).where(Account.id == state["account_id"]))
        account = result.scalars().first()
        if account:
            return {
                "usage_data": account.usage_data,
                "company_name": account.company_name
            }
    return {}

async def score_churn(state: RetentionState):
    """
    Node 2 -- score_churn
    call retention_service, compute score
    """
    usage_data = state.get("usage_data", {})
    risk_info = compute_retention_risk(usage_data)
    return {
        "churn_score": risk_info["churn_score"],
        "churn_reason_system": risk_info["churn_reason"],
        "intervention": risk_info.get("intervention_recommendation", "None")
    }

async def classify_reason(state: RetentionState):
    """
    Node 3 -- classify_reason
    call Claude with signals -> 1-sentence churn reason
    """
    llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0).with_structured_output(ChurnReasonResult)
    usage_str = json.dumps(state.get("usage_data", {}), indent=2)
    prompt = f"Given this usage data for {state.get('company_name', 'the client')}:\n{usage_str}\n\nProvide a 1-sentence explanation of the primary churn risk."
    try:
        res = await llm.ainvoke([HumanMessage(content=prompt)])
        return {"churn_reason_ai": res.reason}
    except Exception as e:
        logger.error(f"Error in classify_reason: {e}")
        return {"churn_reason_ai": state.get("churn_reason_system", "Usage drops detected.")}

async def generate_intervention(state: RetentionState):
    """
    Node 4 -- generate_intervention
    Recommend action & generate outreach email draft only if score > 40
    """
    score = state.get("churn_score", 0)
    if score <= 40:
        return {"email_draft": ""}
        
    llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0.7).with_structured_output(InterventionResult)
    prompt = f"""
    The account {state.get('company_name', 'Customer')} is at risk of churn.
    Churn Score: {score}/100
    Risk factors: {state.get('churn_reason_ai') or state.get('churn_reason_system')}
    Suggested broad intervention: {state.get('intervention')}
    
    Write an empathetic, proactive customer success email check-in draft to address this. Do not sound alarming, but focus on getting them value.
    Also provide a brief internal recommendation.
    """
    try:
        res = await llm.ainvoke([HumanMessage(content=prompt)])
        return {
            "email_draft": res.email_draft,
            "intervention": res.recommendation
        }
    except Exception as e:
        logger.error(f"Error in generate_intervention: {e}")
        return {"email_draft": "Hi there, \n\nWe noticed some changes in your usage and wanted to check in. Let's schedule a time to chat."}

async def update_account(state: RetentionState):
    """
    Node 5 -- update_account
    Save churn_score, churn_reason, intervention
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Account).where(Account.id == state["account_id"]))
        account = result.scalars().first()
        if account:
            account.churn_score = state.get("churn_score", 0)
            account.churn_reason = state.get("churn_reason_ai") or state.get("churn_reason_system")
            if state.get("email_draft"):
                account.intervention_status = state.get("intervention", "intervention_required")
                usage_data = dict(account.usage_data or {})
                usage_data["latest_intervention_draft"] = state.get("email_draft")
                account.usage_data = usage_data
            else:
                account.intervention_status = "healthy"
                
            await session.commit()
            
            try:
                log = AgentLog(
                    org_id=account.org_id,
                    agent_type="retention_agent",
                    action="scored_churn_risk",
                    status="success",
                    metadata={
                        "account_id": str(account.id),
                        "score": account.churn_score,
                        "reason": account.churn_reason
                    }
                )
                session.add(log)
                await session.commit()
            except Exception as e:
                logger.error(f"Failed to log retention agent action: {e}")
    return {}

# Define Graph
def build_retention_agent():
    workflow = StateGraph(RetentionState)
    
    workflow.add_node("gather_signals", gather_signals)
    workflow.add_node("score_churn", score_churn)
    workflow.add_node("classify_reason", classify_reason)
    workflow.add_node("generate_intervention", generate_intervention)
    workflow.add_node("update_account", update_account)
    
    workflow.set_entry_point("gather_signals")
    
    workflow.add_edge("gather_signals", "score_churn")
    workflow.add_edge("score_churn", "classify_reason")
    
    def should_intervene(state: RetentionState):
        if state.get("churn_score", 0) > 40:
            return "generate_intervention"
        return "update_account"
        
    workflow.add_conditional_edges(
        "classify_reason",
        should_intervene,
        {"generate_intervention": "generate_intervention", "update_account": "update_account"}
    )
    
    workflow.add_edge("generate_intervention", "update_account")
    workflow.add_edge("update_account", END)
    
    return workflow.compile()

async def run_retention_agent(account_id: str, org_id: str):
    app = build_retention_agent()
    initial_state = {
        "account_id": account_id,
        "org_id": org_id,
    }
    result = await app.ainvoke(initial_state)
    return result
