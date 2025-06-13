from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Deliverable(Base):
    __tablename__ = "deliverables"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String(20), nullable=False, default="IN_PLANNING")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    project_id = Column(String(36), ForeignKey("tkse.projects.id"))

    project = relationship("Project", back_populates="deliverables")
    tasks = relationship("Task", back_populates="deliverable")

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    estimated_time = Column(Float)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deliverable_id = Column(String(36), ForeignKey("tkse.deliverables.id"))

    deliverable = relationship("Deliverable", back_populates="tasks")
    acceptance_criteria = relationship(
        "AcceptanceCriteria",
        back_populates="task",
        cascade="all, delete-orphan",
        single_parent=True
    )

class AcceptanceCriteria(Base):
    __tablename__ = "acceptance_criteria"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    task_id = Column(String(36), ForeignKey("tkse.tasks.id"))

    task = relationship("Task", back_populates="acceptance_criteria")
    
class TaskSubmission(Base):
    __tablename__ = "task_submissions"
    __table_args__ = {"schema": "tkse"}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey("tkse.tasks.id"), nullable=False)
    student_id = Column(String(36), ForeignKey("tkse.students.id"), nullable=False)
    validated_by = Column(String(36), ForeignKey("tkse.enterprises.id"), nullable=True)

    submission_link = Column(String(500), nullable=True)
    branch_name = Column(String(255), nullable=True)
    evidence_file = Column(String(500), nullable=True)
    status = Column(String(20), default="PENDING")
    feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    validated_at = Column(DateTime(timezone=True), nullable=True)

    task = relationship("Task")
    student = relationship("Student")
    validator = relationship("Enterprise", foreign_keys=[validated_by])