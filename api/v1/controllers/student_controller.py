from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.v1.schemas.student_schema import StudentCreate, StudentRead
from api.v1.services import student_service
from db.session import get_db

router = APIRouter()

@router.post("/", response_model=StudentRead)
def create_student_view(student: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db, student)

@router.get("/", response_model=List[StudentRead])
def get_students(db: Session = Depends(get_db)):
    return student_service.list_students(db)


@router.delete("/{student_id}", response_model=StudentRead)
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
    deleted = student_service.remove_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return deleted

@router.get("/{student_id}/projects")
def get_projects_by_student(student_id: UUID, db: Session = Depends(get_db)):
    return student_service.get_projects_by_student(db, student_id)
