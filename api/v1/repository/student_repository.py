from fastapi import HTTPException
from db.models.project import Project
from db.models.student import Student
from db.models.task import Task, Deliverable
import uuid
from datetime import datetime, timezone
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload, Session
from passlib.context import CryptContext
from api.v1.schemas.student_schema import StudentUpdate
from db.models.student_project import StudentProject

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_student_by_id(db: Session, student_id: str):
    return db.query(Student).filter(Student.id == student_id, Student.is_active == True).first()

def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email, Student.is_active == True).first()

def get_student_with_projects_and_deliverables(db: Session, student_id: str):
    """Busca o aluno com seus projetos, entregáveis e tasks de cada entregável."""
    return db.query(Student).options(
        joinedload(Student.student_projects)
            .joinedload(StudentProject.project)
            .joinedload(Project.deliverables)
            .joinedload(Deliverable.tasks)
            .joinedload(Task.acceptance_criteria)
    ).filter(Student.id == student_id, Student.is_active == True).first()

def get_student_deliverables_list(db: Session, student_id: str):
    """Extrai a lista de entregáveis dos projetos do aluno."""
    student = get_student_with_projects_and_deliverables(db, student_id)
    if not student:
        return None
    deliverables = []
    for sp in student.student_projects:
        if sp.project:
            deliverables.extend(sp.project.deliverables)
    return deliverables

def get_student_with_projects(db: Session, student_id: str):
    """Busca estudante com seus projetos relacionados"""
    return db.query(Student).options(
        joinedload(Student.student_projects).joinedload(StudentProject.project)
    ).filter(Student.id == student_id, Student.is_active == True).first()
        
def repo_create_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_all_students(db: Session, enterprise_id: str):
    subquery = (
        db.query(
            StudentProject.student_id,
            func.count(Project.id).label("project_count")
        )
        .join(Project, Project.id == StudentProject.project_id)
        .filter(Project.enterprise_id == enterprise_id)
        .group_by(StudentProject.student_id)
        .subquery()
    )

    result = (
        db.query(Student, subquery.c.project_count)
        .join(subquery, Student.id == subquery.c.student_id)  # <-- INNER JOIN 
        .filter(Student.is_active == True)
        .all()
    )

    return [
        {
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
            "welcome": student.welcome,
            "is_active": student.is_active,
            "created_at": student.created_at,
            "updated_at": student.updated_at,
            "project_count": project_count
        }
        for student, project_count in result
    ]
    
def get_all_students_by_project(db: Session, student_id: str):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    projects = [
        sp.project for sp in student.student_projects
    ]

    return projects

def link_student_to_project(db: Session, student_id: uuid.UUID, project_id: uuid.UUID):
    print(f"Trying to link student {student_id} to project {project_id}")

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.status in ("PENDING", "CANCELLED"):
        raise HTTPException(
            status_code=400,
            detail="Cannot join a project that has not started or has been cancelled"
        )

    student_project = StudentProject(
        student_id=student.id,
        project_id=project.id,
    )

    db.add(student_project)
    db.commit()
    db.refresh(student_project)

    return student_project

def get_all_students_with_projects(db: Session):
    """Lista todos os estudantes com seus projetos"""
    return db.query(Student).options(
        joinedload(Student.student_projects).joinedload(StudentProject.project)
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
