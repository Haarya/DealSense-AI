from sqlalchemy import String, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, UUIDMixin
import uuid
from datetime import datetime

class Battlecard(Base, UUIDMixin):
    __tablename__ = "battlecards"

    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True, nullable=False)
    competitor_name: Mapped[str] = mapped_column(String, nullable=False)
    strengths: Mapped[str] = mapped_column(Text, nullable=False)
    weaknesses: Mapped[str] = mapped_column(Text, nullable=False)
    positioning: Mapped[str] = mapped_column(Text, nullable=False)
    objection_handlers: Mapped[list] = mapped_column(JSONB, default=[], server_default='[]')
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
