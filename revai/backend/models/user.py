from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, UUIDMixin
import uuid

class Organization(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    crm_type: Mapped[str] = mapped_column(String, default="none", nullable=False)
    hubspot_access_token: Mapped[str | None] = mapped_column(String, nullable=True)

    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")


class User(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True, nullable=False)
    role: Mapped[str] = mapped_column(String, default="member", nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    organization = relationship("Organization", back_populates="users")
