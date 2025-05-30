from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import joinedload, Session
from passlib.context import CryptContext

from api.v1.schemas.student_schema import StudentCreate, StudentUpdate
from db.models.student import Student

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_student_by_id(db: Session, student_id: str):
    return db.query(Student).filter(Student.id == student_id, Student.is_active == True).first()

def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email, Student.is_active == True).first()

def get_student_with_projects(db: Session, student_id: str):
    """Busca estudante com seus projetos relacionados"""
    return db.query(Student).options(
        joinedload(Student.student_projects).joinedload("project")
    ).filter(Student.id == student_id, Student.is_active == True).first()
        
def create_student(db: Session, student: StudentCreate):
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                )
    
    # Criptografar a senha antes de salvar
    hashed_password = pwd_context.hash(student.password)
    
    db_student = Student(
        name=student.name,
        email=student.email,
        password=hashed_password,
        phone=student.phone,
        role=student.role,
        location=student.location,
        photo=student.photo,
        cargo=student.cargo,
        bio=student.bio,
        github=student.github,
        linkedin=student.linkedin,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_all_students(db: Session):
    return db.query(Student).filter(Student.is_active == True).all()

def get_all_students_with_projects(db: Session):
    """Lista todos os estudantes com seus projetos"""
    return db.query(Student).options(
        joinedload(Student.student_projects).joinedload("project")
    ).filter(Student.is_active == True).all()

def update_student(db: Session, student_id: str, data: StudentUpdate) -> Student:
    student = db.query(Student).filter(Student.id == student_id, Student.is_active == True).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if data.email:
        existing_email = db.query(Student).filter(
            and_(Student.email == data.email, Student.id != student_id, Student.is_active == True)
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="E-mail is already in use")

    # Se a senha está sendo atualizada, criptografar
    update_data = data.model_dump(exclude_unset=True)
    if 'password' in update_data:
        update_data['password'] = pwd_context.hash(update_data['password'])

    for field, value in update_data.items():
        setattr(student, field, value)
        
    student.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: str) -> Student:
    student = db.query(Student).filter(Student.id == student_id, Student.is_active == True).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found or already inactive")
    
    student.is_active = False
    student.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(student)
    return student