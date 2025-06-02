from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class EnterpriseBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    country_id: Optional[str] = None
    cnpj: Optional[str] = None
    legal_name: Optional[str] = None
    trade_name: Optional[str] = None
    state_registration: Optional[str] = None
    municipal_registration: Optional[str] = None
    responsible_person: Optional[str] = None


class EnterpriseCreate(EnterpriseBase):
    email: EmailStr
    password: str


class EnterpriseUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    country_id: Optional[str] = None
    cnpj: Optional[str] = None
    legal_name: Optional[str] = None
    trade_name: Optional[str] = None
    state_registration: Optional[str] = None
    municipal_registration: Optional[str] = None
    responsible_person: Optional[str] = None


class EnterpriseResponse(EnterpriseBase):
    id: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
    
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: EnterpriseResponse
