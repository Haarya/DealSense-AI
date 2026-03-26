from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin, UUIDMixin
import uuid

class AgentLog(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "agent_logs"

    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True, nullable=False)
    agent_type: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    metadata_info: Mapped[dict] = mapped_column("metadata", JSONB, default={}, server_default='{}')
