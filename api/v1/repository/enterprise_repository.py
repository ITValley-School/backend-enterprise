from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api.v1.schemas.enterprise_schema import EnterpriseCreateForm, EnterpriseResponse, EnterpriseUpdate
from db.models.enterprise import Enterprise
from db.models.project import Project
from db.models.student_project import StudentProject

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


def create_enterprise(db: Session, enterprise: EnterpriseCreateForm):
    try:
        existing = db.query(Enterprise).filter(Enterprise.email == enterprise.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )


        db.add(enterprise)
        db.commit()
        db.refresh(enterprise)
        return enterprise
    finally:
        db.close()


def update_enterprise(db: Session, enterprise_id: UUID, data: EnterpriseCreateForm) -> Enterprise:
    try:
        enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
        if not enterprise:
            raise HTTPException(status_code=404, detail="Enterprise not found")

        if data.cnpj:
            existing = db.query(Enterprise).filter(
                and_(Enterprise.cnpj == data.cnpj, Enterprise.id != enterprise_id)
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="CNPJ is already in use")

        if data.email:
            existing_email = db.query(Enterprise).filter(
                and_(Enterprise.email == data.email, Enterprise.id != enterprise_id)
            ).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="E-mail is already in use")

        for field, value in data.__dict__.items():
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

def list_enterprises_by_student(db: Session, student_id: UUID):
    """
    Retorna todas as enterprises relacionadas a um student (onde ele participa de projetos).
    """
    query = (
        db.query(Enterprise)
        .join(Project, Project.enterprise_id == Enterprise.id)
        .join(StudentProject, StudentProject.project_id == Project.id)
        .filter(StudentProject.student_id == student_id)
        .filter(Enterprise.is_active == True)
        .distinct()
    )

    enterprises = query.all()

    return [EnterpriseResponse.model_validate(e) for e in enterprises]