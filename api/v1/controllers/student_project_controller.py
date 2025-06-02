from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.student_project_schema import StudentProjectCreate, StudentProjectRead
from services import student_project_service

router = APIRouter()

@router.post("/student-projects", response_model=StudentProjectRead)
def assign_student_to_project(link: StudentProjectCreate, db: Session = Depends(get_db)):
    return student_project_service.assign_student_to_project(db, link)
