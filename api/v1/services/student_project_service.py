from sqlalchemy.orm import Session
from repository import student_project_repository
from schemas.student_project_schema import StudentProjectCreate

def assign_student_to_project(db: Session, assignment: StudentProjectCreate):
    return student_project_repository.create_student_project(db, assignment)
