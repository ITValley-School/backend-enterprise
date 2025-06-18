from sqlalchemy.orm import Session
from api.v1.schemas.student_project_schema import StudentProjectCreate
from api.v1.repository.student_project_repository import create_student_project

def assign_student_to_project(db: Session, link: StudentProjectCreate):
    return create_student_project(db=db, link=link)
