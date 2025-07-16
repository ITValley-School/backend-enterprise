from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from db.base import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = {"schema": "tkse"}

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4, nullable=False)
    from_id = Column(String(36), nullable=False)
    to_id = Column(String(36), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)