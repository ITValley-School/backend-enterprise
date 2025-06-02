from pydantic import BaseModel
from datetime import datetime

class StudentProjectBase(BaseModel):
    student_id: str
    project_id: str

class StudentProjectCreate(StudentProjectBase):
    pass

class StudentProjectRead(StudentProjectBase):
    id: int
    joined_at: datetime

    model_config = {
        "from_attributes": True
    }