from sqlalchemy import String, ForeignKey, Integer, Date, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin, UUIDMixin
import uuid
from datetime import date

class Account(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "accounts"

    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String, nullable=False)
    mrr: Mapped[float] = mapped_column(Numeric, nullable=False)
    contract_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    churn_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    churn_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    usage_data: Mapped[dict] = mapped_column(JSONB, default={}, server_default='{}')
    intervention_status: Mapped[str] = mapped_column(String, default="none", nullable=False)
