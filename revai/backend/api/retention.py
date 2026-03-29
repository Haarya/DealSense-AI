from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from database import get_db
from models.account import Account
from utils.auth import get_current_user
from schemas.auth import UserResponse
from schemas.retention import AccountResponse, AccountListResponse, InterveneResponse

# For manual triggering
from agents.retention_agent import run_retention_agent

router = APIRouter(prefix="/retention", tags=["retention"])

@router.get("/accounts", response_model=AccountListResponse)
async def get_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    query = select(Account).where(Account.org_id == current_user.org_id)
    
    # Get total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # Get paginated items
    query = query.order_by(Account.churn_score.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    accounts = result.scalars().all()
    
    return {"items": accounts, "total": total or 0}

@router.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    result = await db.execute(
        select(Account).where(
            Account.id == account_id,
            Account.org_id == current_user.org_id
        )
    )
    account = result.scalars().first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    return account

@router.post("/intervene/{account_id}", response_model=InterveneResponse)
async def trigger_intervention(
    account_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    # Verify account belongs to org
    result = await db.execute(
        select(Account).where(
            Account.id == account_id,
            Account.org_id == current_user.org_id
        )
    )
    account = result.scalars().first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    # Trigger the agent
    agent_result = await run_retention_agent(str(account.id), str(current_user.org_id))
    
    # Reload account to get updated data
    await db.refresh(account)
    
    return {
        "account_id": account.id,
        "email_draft": account.usage_data.get("latest_intervention_draft", ""),
        "intervention": account.intervention_status
    }
