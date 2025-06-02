import uuid
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime, timezone

class StudentProject(Base):
    __tablename__ = "student_project"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    student_id = Column(String(36), ForeignKey("tkse.students.id", ondelete="CASCADE"))
    project_id = Column(String(36), ForeignKey("tkse.projects.id", ondelete="CASCADE"))
    joined_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="student_projects", overlaps="projects,students")
    project = relationship("Project", back_populates="student_projects", overlaps="student_projects,students,projects")
