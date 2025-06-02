from sqlalchemy.orm import Session
from db.models.student_project import StudentProject
from schemas.student_project_schema import StudentProjectCreate

def create_student_project(db: Session, link: StudentProjectCreate):
    student_project = StudentProject(
        student_id=link.student_id,
        project_id=link.project_id
    )
    db.add(student_project)
    db.commit()
    db.refresh(student_project)
    return student_project
