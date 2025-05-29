from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from db.base import Base

class Student(Base):
    __tablename__ = "students"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=True)
    location = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relacionamento com a tabela pivot
    student_projects = relationship("StudentProject", back_populates="student", cascade="all, delete-orphan", overlaps="projects,students,student_projects")

