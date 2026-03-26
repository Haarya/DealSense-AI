from sqlalchemy import String, ForeignKey, Integer, Date, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, UUIDMixin
import uuid
from datetime import date

class Deal(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "deals"

    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True, nullable=False)
    crm_deal_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[float] = mapped_column(Numeric, nullable=False)
    stage: Mapped[str] = mapped_column(String, nullable=False)
    close_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    health_score: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    risk_signals: Mapped[list] = mapped_column(JSONB, default=[], server_default='[]')
    last_contact_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    assigned_to: Mapped[str | None] = mapped_column(String, nullable=True)

    alerts = relationship("DealAlert", back_populates="deal", cascade="all, delete-orphan")


class DealAlert(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "deal_alerts"

    deal_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("deals.id", ondelete="CASCADE"), index=True, nullable=False)
    alert_type: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    recovery_play: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="open", nullable=False)

    deal = relationship("Deal", back_populates="alerts")
