from uuid import UUID
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from api.v1.repository.enterprise_repository import delete_enterprise, update_enterprise
from api.v1.schemas.enterprise_schema import EnterpriseUpdate

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def update_enterprise_service(db: Session, enterprise_id: UUID, data: EnterpriseUpdate):
    enterprise = update_enterprise(db, enterprise_id, data)
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return enterprise


def delete_enterprise_service(db: Session, enterprise_id: UUID):
    success = delete_enterprise(db, enterprise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Enterprise not found")
