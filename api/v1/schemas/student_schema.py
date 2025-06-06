from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class StudentLoginRequest(BaseModel):
    email: EmailStr
    password: str

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    photo: Optional[str] = None
    cargo: Optional[str] = None
    bio: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None

class StudentResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    photo: Optional[str] = None
    cargo: Optional[str] = None
    bio: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class StudentTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    student: StudentResponse

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    photo: Optional[str] = None
    cargo: Optional[str] = None
    bio: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None

StudentRead = StudentResponse

class StudentDashboardResponse(BaseModel):
    completed_tasks: int
    in_progress_tasks: int
    total_deliverables: int
    certificate: int
