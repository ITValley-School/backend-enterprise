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
