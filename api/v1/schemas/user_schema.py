from typing import Optional
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserUpdate(BaseModel):
    name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]