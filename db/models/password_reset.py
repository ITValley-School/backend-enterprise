from datetime import datetime, timezone, timedelta
import uuid
from sqlalchemy import Column, DateTime, String, Text, Enum
from sqlalchemy.orm import relationship
from db.base import Base
import enum


class UserType(enum.Enum):
    ENTERPRISE = "enterprise"
    STUDENT = "student"


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    user_id = Column(String(36), nullable=False)
    is_used = Column(String(10), default="false", nullable=False)  # "true" ou "false"
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(hours=1), nullable=False)

    @property
    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_valid(self):
        return not self.is_expired and self.is_used == "false" 