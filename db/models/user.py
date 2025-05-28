from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, String
from db.base import Base



class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(150), nullable=False)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)