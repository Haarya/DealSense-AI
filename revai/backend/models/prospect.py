from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, UUIDMixin
import uuid

class Prospect(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "prospects"

    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String, nullable=False)
    domain: Mapped[str] = mapped_column(String, nullable=False)
    contact_name: Mapped[str] = mapped_column(String, nullable=False)
    contact_email: Mapped[str] = mapped_column(String, nullable=False)
    contact_linkedin: Mapped[str | None] = mapped_column(String, nullable=True)
    icp_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String, default="researching", nullable=False)
    fit_signals: Mapped[list] = mapped_column(JSONB, default=[], server_default='[]')

    sequences = relationship("Sequence", back_populates="prospect", cascade="all, delete-orphan")


class Sequence(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "sequences"

    prospect_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("prospects.id", ondelete="CASCADE"), index=True, nullable=False)
    steps: Mapped[list] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String, default="draft", nullable=False)
    current_step: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    prospect = relationship("Prospect", back_populates="sequences")
