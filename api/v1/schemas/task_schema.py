from datetime import datetime
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from api.v1.schemas.enterprise_schema import EnterpriseResponse


class TaskSubmissionCreate(BaseModel):
    task_id: str
    submission_link: str
    branch_name: Optional[str]
    evidence_file: Optional[str]  # caminho para arquivo salvo

class TaskSubmissionValidate(BaseModel):
    validator_id: str
    status: Literal["APPROVED", "REJECTED"]
    feedback: Optional[str] = None

class TaskSubmissionResponse(BaseModel):
    id: str
    task_id: str
    student_id: str
    submission_link: str
    branch_name: Optional[str]
    evidence_file: Optional[str]
    status: str
    feedback: Optional[str]
    submitted_at: datetime
    validated_at: Optional[datetime]
    validator: Optional[EnterpriseResponse]

    model_config = {"from_attributes": True}

class TaskBasicInfo(BaseModel):
    id: str
    name: str
    description: str
    status: str
    estimated_time: Optional[float]

    model_config = {"from_attributes": True}

class StudentSubmissionResponse(BaseModel):
    id: str
    task_id: str
    submission_link: Optional[str]
    branch_name: Optional[str]
    evidence_file: Optional[str]
    status: str
    feedback: Optional[str]
    submitted_at: datetime
    validated_at: Optional[datetime]
    task: TaskBasicInfo
    validator: Optional[EnterpriseResponse]

    model_config = {"from_attributes": True}
