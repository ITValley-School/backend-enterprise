from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.v1.schemas.student_schema import StudentCreate
from db.models.project import Project
from db.models.student import Student
import uuid

from db.models.student_project import StudentProject

def create_student(db: Session, student: StudentCreate):
    db_student = Student(
        id=str(uuid.uuid4()),
        name=student.name,
        email=student.email,
        password=student.password,
        phone=student.phone,
        role=student.role,
        location=student.location
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

def get_all_students(db: Session):
    return db.query(Student).all()

def delete_student(db: Session, student_id: str):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
    return student

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

    student_project = StudentProject(
        student_id=student.id,
        project_id=project.id,
    )

    db.add(student_project)
    db.commit()
    db.refresh(student_project)

    return student_project
