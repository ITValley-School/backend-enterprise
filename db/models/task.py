from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Deliverable(Base):
    __tablename__ = "deliverables"
    __table_args__ = {"schema": "tkse"}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("tkse.projects.id"))

    project = relationship("Project", back_populates="deliverables")
    tasks = relationship("Task", back_populates="deliverable")

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"schema": "tkse"}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    estimated_time = Column(Float)
    deliverable_id = Column(Integer, ForeignKey("tkse.deliverables.id"))

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

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey("tkse.tasks.id"))

    task = relationship("Task", back_populates="acceptance_criteria")
