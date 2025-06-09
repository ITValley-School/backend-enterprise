from datetime import datetime
from typing import Optional
from fastapi import File, Form, UploadFile
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

class EnterpriseCreateForm:
    def __init__(
        self,
        name: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...),
        cnpj: str = Form(...),
        phone: str = Form(...),
        website: str = Form(...),
        address: str = Form(...),
        city: str = Form(...),
        state: str = Form(...),
        zip_code: str = Form(...),
        responsible_person: str = Form(...),
        country_id: Optional[str] = Form(None),
        profile_image: Optional[UploadFile] = File(None),
        remove_image: Optional[bool] = Form(False),
    ):
        self.name = name
        self.email = email
        self.password = password
        self.cnpj = cnpj
        self.phone = phone
        self.website = website
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.responsible_person = responsible_person
        self.country_id = country_id
        self.profile_image = profile_image
        self.remove_image = remove_image

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
    profile_image_path: Optional[str]

    model_config = {
        "from_attributes": True
    }
    
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: EnterpriseResponse
