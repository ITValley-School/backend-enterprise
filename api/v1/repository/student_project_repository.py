from sqlalchemy.orm import Session
from api.v1.schemas.student_project_schema import StudentProjectCreate
from db.models.student_project import StudentProject

def create_student_project(db: Session, link: StudentProjectCreate):
    student_project = StudentProject(
        student_id=link.student_id,
        project_id=link.project_id
    )
    db.add(student_project)
    db.commit()
    db.refresh(student_project)
    return student_project
