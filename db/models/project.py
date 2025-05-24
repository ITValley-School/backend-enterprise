from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
from db.models.task import Deliverable



class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": "tkse"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    blob_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    deliverables = relationship(Deliverable, back_populates="project", cascade="all, delete-orphan")
