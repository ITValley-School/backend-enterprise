from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }