from uuid import UUID
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

from api.v1.repository.user_repository import delete_user, update_user
from api.v1.schemas.user_schema import UserUpdate

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)  + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def update_user_service(user_id: UUID, data: UserUpdate):
    user = update_user(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user_service(user_id: UUID):
    success = delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
