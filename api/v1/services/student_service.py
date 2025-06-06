from sqlalchemy.orm import Session
from api.v1.repository import student_repository
from api.v1.repository.student_repository import (
    create_student as repo_create_student,
    get_student_by_id,
    get_all_students,
    get_student_deliverables_list,
    update_student as repo_update_student,
    delete_student as repo_delete_student
)
from api.v1.schemas.student_schema import StudentCreate, StudentUpdate
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

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

def create_student(db: Session, student_data: StudentCreate):
    return repo_create_student(db, student_data)

def list_students(db: Session):
    return get_all_students(db)

def get_student_by_id_service(db: Session, student_id: str):
    student = get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def update_student_service(db: Session, student_id: str, data: StudentUpdate):
    student = repo_update_student(db, student_id, data)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def delete_student_service(db: Session, student_id: str):
    success = repo_delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")

def get_projects_by_student(db: Session, student_id: str):
    return student_repository.get_all_students_by_project(db, student_id)

def link_student_to_project(db: Session, student_id: str, project_id: str):
    return student_repository.link_student_to_project(db, student_id, project_id)


def list_deliverables_for_student(db: Session, student_id: str):
    deliverables = get_student_deliverables_list(db, student_id)
    if deliverables is None:
        raise Exception("Student not found or inactive")
    return deliverables