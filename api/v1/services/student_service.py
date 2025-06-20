from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from api.v1.repository import student_repository
from api.v1.repository.student_repository import (
    get_student_by_id,
    get_all_students,
    repo_create_student,
    get_student_deliverables_list,
    update_student as repo_update_student,
    delete_student as repo_delete_student
)
from api.v1.schemas.student_schema import StudentCreateForm, StudentUpdate, StudentDeliverableResponse, StudentUpdateForm
from fastapi import HTTPException, UploadFile, status
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

from db.models.student import Student

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

def create_student_service(data: StudentCreateForm, db: Session):
    existing = db.query(Student).filter(Student.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    hashed_password = pwd_context.hash(data.password)
    image_path = handle_image_upload(data.profile_image)

    db_student = Student(
        name=data.name,
        email=data.email,
        password=hashed_password,
        phone=data.phone,
        role=data.role,
        location=data.location,
        cargo=data.cargo,
        bio=data.bio,
        github=data.github,
        linkedin=data.linkedin,
        photo=image_path,
    )

    return repo_create_student(db, db_student)


def list_students(db: Session):
    return get_all_students(db)

def get_student_by_id_service(db: Session, student_id: str):
    student = get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def update_student_service(student_id: UUID, data: StudentUpdateForm, db: Session):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = data.name
    student.email = data.email
    student.phone = data.phone
    student.role = data.role or student.role
    student.location = data.location
    student.cargo = data.cargo
    student.bio = data.bio
    student.github = data.github
    student.linkedin = data.linkedin
    
    if data.remove_image:
        student.photo = None

    # Só atualiza senha se for enviada
    if data.password:
        student.password = pwd_context.hash(data.password)

    # Atualiza imagem se enviada
    if data.profile_image:
        student.photo = handle_image_upload(data.profile_image)


    db.commit()
    db.refresh(student)
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
    
    # Formatando os deliverables com o novo schema que inclui tasks
    formatted_deliverables = []
    for deliverable in deliverables:
        formatted_deliverable = StudentDeliverableResponse.model_validate(deliverable)
        formatted_deliverables.append(formatted_deliverable)
    
    return formatted_deliverables


def handle_image_upload(image: UploadFile, base_path="static/uploads/students/"):
    if not image:
        return None
    ext = image.filename.split(".")[-1]
    filename = f"{uuid4().hex}_{datetime.utcnow().timestamp()}.{ext}"
    os.makedirs(base_path, exist_ok=True)
    file_path = os.path.join(base_path, filename)
    with open(file_path, "wb") as f:
        f.write(image.file.read())
    return file_path