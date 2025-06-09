from pydantic import BaseModel, EmailStr
from typing import Optional


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ForgotPasswordResponse(BaseModel):
    message: str
    email: EmailStr


class ResetPasswordResponse(BaseModel):
    message: str


class EmailTestRequest(BaseModel):
    to_email: EmailStr
    subject: str
    message: str 