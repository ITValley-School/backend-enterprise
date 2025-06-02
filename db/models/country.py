from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship
from db.base import Base

class Country(Base):
    __tablename__ = "countries"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    flag_image = Column(String(500), nullable=True)
    code = Column(String(3), nullable=True, unique=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    enterprises = relationship("Enterprise", back_populates="country_info") 