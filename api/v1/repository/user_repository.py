from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import and_
from api.v1.schemas.user_schema import UserCreate, UserUpdate
from db.session import SessionLocal
from db.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_id(user_id: int):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()

def get_user_by_username(username: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()

def get_user_by_email(email: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()
        
def create_user(user: UserCreate):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already exists",
                    )
        
        hashed_password = pwd_context.hash(user.password)
        
        db_user = User(
            name=user.name,
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    finally:
        db.close()

def update_user(user_id: UUID, data: UserUpdate) -> User:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if data.username:
            existing = db.query(User).filter(
                and_(
                    User.username == data.username,
                    User.id != user_id
                )
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Username is already in use")
            
        if data.email:
            existing_email = db.query(User).filter(
                and_(User.email == data.email, User.id != user_id)
            ).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="E-mail is already in use")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
            
        user.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

def delete_user(user_id: UUID) -> bool:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found or already inactive")
        
        user.is_active = False
        user.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()
