from fastapi import File, Form, UploadFile
from pydantic import BaseModel, EmailStr
from typing import Optional, List
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
    welcome: Optional[bool] = True

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
    welcome: bool
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

class StudentLogoutResponse(BaseModel):
    message: str
    logged_out_at: datetime

    model_config = {
        "from_attributes": True
    }

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
    welcome: Optional[bool] = None

StudentRead = StudentResponse

class StudentDashboardResponse(BaseModel):
    completed_tasks: int
    in_progress_tasks: int
    total_deliverables: int
    certificate: int

class StudentAcceptanceCriteriaResponse(BaseModel):
    id: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class StudentTaskResponse(BaseModel):
    id: str
    name: str
    description: str
    status: str
    estimated_time: Optional[float]
    created_at: datetime
    updated_at: datetime
    acceptance_criteria: List[StudentAcceptanceCriteriaResponse]

    model_config = {
        "from_attributes": True
    }

class StudentDeliverableResponse(BaseModel):
    id: str
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    project_id: str
    tasks: List[StudentTaskResponse]

    model_config = {
        "from_attributes": True
    }

class StudentCreateForm(BaseModel):
    name: str = Form(...)
    email: str = Form(...)
    password: str = Form(...)
    phone: str = Form(...)
    role: str = Form(...)
    location: str = Form(...)
    cargo: str = Form(...)
    bio: str = Form(...)
    github: str = Form(...)
    linkedin: str = Form(...)
    profile_image: Optional[UploadFile] = None

class StudentUpdateForm(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    cargo: Optional[str] = None
    bio: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    profile_image: Optional[UploadFile] = None
    remove_image: Optional[bool] = Form(False)

class StudentProjectResponse(BaseModel):
    """Schema para projeto na resposta dos projetos do estudante"""
    id: str
    name: str
    description: str
    technologies: List[str]
    complexity: str
    category: str
    score: str
    country: str
    status: str
    joined_at: datetime
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class StudentProjectsResponse(BaseModel):
    """Schema para resposta completa dos projetos do estudante"""
    student_id: str
    student_name: str
    projects: List[StudentProjectResponse]

    model_config = {
        "from_attributes": True
    }