from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CountryBase(BaseModel):
    name: str
    flag_image: Optional[str] = None
    code: Optional[str] = None

class CountryCreate(CountryBase):
    pass

class CountryUpdate(BaseModel):
    name: Optional[str] = None
    flag_image: Optional[str] = None
    code: Optional[str] = None

class CountryResponse(CountryBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 