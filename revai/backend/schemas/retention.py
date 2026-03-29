from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict
from datetime import date
from uuid import UUID

class AccountBase(BaseModel):
    company_name: str
    mrr: float
    contract_end_date: Optional[date] = None

class AccountResponse(AccountBase):
    id: UUID
    org_id: UUID
    churn_score: int
    churn_reason: Optional[str]
    intervention_status: str
    usage_data: Dict

    model_config = ConfigDict(from_attributes=True)

class AccountListResponse(BaseModel):
    items: list[AccountResponse]
    total: int

class InterveneResponse(BaseModel):
    account_id: UUID
    email_draft: Optional[str] = None
    intervention: str

class TaskResponse(BaseModel):
    task_id: str
    status: str
