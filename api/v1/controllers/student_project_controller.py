from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from api.v1.schemas.student_project_schema import StudentProjectCreate, StudentProjectRead
from api.v1.repository.student_project_repository import create_student_project

router = APIRouter()

@router.post("/", response_model=StudentProjectRead)
def create_student_project_link(
    link: StudentProjectCreate,
    db: Session = Depends(get_db)
):
    return create_student_project(db=db, link=link)
