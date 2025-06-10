from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.orm import relationship
from db.base import Base

class Student(Base):
    __tablename__ = "students"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    phone = Column(String(50), nullable=True)
    role = Column(String(100), nullable=True)
    location = Column(String(200), nullable=True)
    photo = Column(String(500), nullable=True)
    cargo = Column(String(150), nullable=True)
    bio = Column(Text, nullable=True)
    github = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    welcome = Column(Boolean, default=True, nullable=False)  
    
    # Colunas de controle
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relacionamento com a tabela pivot
    student_projects = relationship("StudentProject", back_populates="student", cascade="all, delete-orphan", overlaps="projects,students")
    projects = relationship("Project", secondary="tkse.student_project", back_populates="students", overlaps="student_projects")
    