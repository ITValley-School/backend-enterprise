from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class VoompSale(BaseModel):
    id: int
    amount: float
    method: str
    status: str
    smart_sale: int

class VoompClient(BaseModel):
    id: int
    city: str
    name: str
    email: str
    street: str
    cellphone: str

class VoompProduct(BaseModel):
    id: int
    name: str

class VoompWebhookPayload(BaseModel):
    sale: VoompSale
    type: str
    client: VoompClient
    product: VoompProduct
    trigger: str
    oldStatus: str
    saleMetas: List[Dict]
    productMetas: Dict[str, str]
    currentStatus: str
    proposalMetas: List[Dict] 