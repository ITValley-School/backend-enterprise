import uuid
from sqlalchemy import JSON, Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db.base import Base
from db.models.task import Deliverable



class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(String(36), ForeignKey("tkse.users.id"), nullable=False)
    blob_path = Column(String, nullable=False)
    description = Column(String, nullable=False)
    technologies = Column(JSON, nullable=False, default=list)
    complexity = Column(String, nullable=False)
    category = Column(String, nullable=False)
    score = Column(String, nullable=False)
    country = Column(String, nullable=False)
    status = Column(String(20), nullable=False, default="Em Aberto")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    owner = relationship("User", back_populates="projects")
    deliverables = relationship(Deliverable, back_populates="project", cascade="all, delete-orphan")
    student_projects = relationship("StudentProject", back_populates="project", cascade="all, delete-orphan", overlaps="students,student_projects")
    students = relationship("Student", secondary="tkse.student_project", back_populates="projects", overlaps="student_projects,projects")
    
    @property
    def progress(self):
        if not self.deliverables:
            return 0
        total = len(self.deliverables)
        concluidas = sum(
            1 for e in self.deliverables if all(t.status == "Concluída" for t in e.tasks)
        )
        return round((concluidas / total) * 100)