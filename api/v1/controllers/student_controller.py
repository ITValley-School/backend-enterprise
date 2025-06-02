from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.v1.services import student_service
from db.session import get_db
from api.v1.schemas.student_schema import (
    StudentLoginRequest, 
    StudentTokenResponse, 
    StudentCreate, 
    StudentResponse, 
    StudentUpdate
)
from api.v1.services.student_service import (
    create_access_token, 
    verify_password, 
    create_student,
    list_students,
    get_student_by_id_service,
    update_student_service, 
    delete_student_service,
)
from api.v1.repository.student_repository import get_student_by_email, get_student_with_projects

router = APIRouter()

@router.post("/login", response_model=StudentTokenResponse)
async def login(data: StudentLoginRequest, db: Session = Depends(get_db)):
    student = get_student_by_email(db, data.email)

    if not student or not verify_password(data.password, student.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = {"sub": str(student.id), "email": student.email}
    token = create_access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "phone": student.phone,
            "role": student.role,
            "location": student.location,
            "photo": student.photo,
            "cargo": student.cargo,
            "bio": student.bio,
            "github": student.github,
            "linkedin": student.linkedin,
            "is_active": student.is_active,
            "created_at": student.created_at,
            "updated_at": student.updated_at
        }
    }

@router.post("/", response_model=StudentResponse)
def create_new_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = get_student_by_email(db, student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_student(db, student)

@router.get("/", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return list_students(db)

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: str, db: Session = Depends(get_db)):
    return get_student_by_id_service(db, student_id)

@router.get("/{student_id}/projects")
def get_student_projects(student_id: str, db: Session = Depends(get_db)):
    """Busca estudante com todos os seus projetos relacionados"""
    student = get_student_with_projects(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    projects = []
    for student_project in student.student_projects:
        project = student_project.project
        projects.append({
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "technologies": project.technologies,
            "complexity": project.complexity,
            "category": project.category,
            "score": project.score,
            "country": project.country,
            "joined_at": student_project.joined_at,
            "created_at": project.created_at
        })
    
    return {
        "student_id": student.id,
        "student_name": student.name,
        "projects": projects
    }

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: str, data: StudentUpdate, db: Session = Depends(get_db)):
    return update_student_service(db, student_id, data)

@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    delete_student_service(db, student_id)

@router.get("/{student_id}/projects")
def get_projects_by_student(student_id: UUID, db: Session = Depends(get_db)):
    return student_service.get_projects_by_student(db, student_id)

@router.post("/{student_id}/projects/{project_id}")
def link_student_to_project(student_id: UUID, project_id: UUID, db: Session = Depends(get_db)):
    return student_service.link_student_to_project(db, student_id, project_id)
