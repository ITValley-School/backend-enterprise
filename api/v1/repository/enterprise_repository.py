from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api.v1.schemas.enterprise_schema import EnterpriseCreate, EnterpriseUpdate
from db.models.enterprise import Enterprise

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_enterprise_by_id(db: Session, enterprise_id: UUID):
    try:
        return db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    finally:
        db.close()


def get_enterprise_by_username(db: Session, username: str):
    try:
        return db.query(Enterprise).filter(Enterprise.username == username).first()
    finally:
        db.close()


def get_enterprise_by_email(db: Session, email: str):
    try:
        return db.query(Enterprise).filter(Enterprise.email == email).first()
    finally:
        db.close()


def create_enterprise(db: Session, enterprise: EnterpriseCreate):
    try:
        existing = db.query(Enterprise).filter(Enterprise.username == enterprise.username).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        hashed_password = pwd_context.hash(enterprise.password)

        db_enterprise = Enterprise(
            **enterprise.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
        )

        db.add(db_enterprise)
        db.commit()
        db.refresh(db_enterprise)
        return db_enterprise
    finally:
        db.close()


def update_enterprise(db: Session, enterprise_id: UUID, data: EnterpriseUpdate) -> Enterprise:
    try:
        enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
        if not enterprise:
            raise HTTPException(status_code=404, detail="Enterprise not found")

        if data.username:
            existing = db.query(Enterprise).filter(
                and_(Enterprise.username == data.username, Enterprise.id != enterprise_id)
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Username is already in use")

        if data.email:
            existing_email = db.query(Enterprise).filter(
                and_(Enterprise.email == data.email, Enterprise.id != enterprise_id)
            ).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="E-mail is already in use")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(enterprise, field, value)

        enterprise.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(enterprise)
        return enterprise
    finally:
        db.close()


def delete_enterprise(db: Session, enterprise_id: UUID) -> bool:
    try:
        enterprise = db.query(Enterprise).filter(
            Enterprise.id == enterprise_id,
            Enterprise.is_active == True
        ).first()

        if not enterprise:
            raise HTTPException(status_code=404, detail="Enterprise not found or already inactive")

        enterprise.is_active = False
        enterprise.deleted_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(enterprise)
        return enterprise
    finally:
        db.close()
