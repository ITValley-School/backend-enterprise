from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship



class Enterprise(Base):
    __tablename__ = "enterprises"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(150), nullable=False)
    cnpj = Column(String(20), unique=True, nullable=True)
    legal_name = Column(String(255), nullable=True)  # razão social
    trade_name = Column(String(255), nullable=True)  # nome fantasia
    state_registration = Column(String(50), nullable=True)  # inscrição estadual
    municipal_registration = Column(String(50), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    country_id = Column(String(36), ForeignKey("tkse.countries.id"), nullable=True)
    responsible_person = Column(String(255), nullable=True)
    hashed_password = Column(String, nullable=False)
    profile_image_path = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    projects = relationship("Project", back_populates="owner")
    country_info = relationship("Country", back_populates="enterprises")
