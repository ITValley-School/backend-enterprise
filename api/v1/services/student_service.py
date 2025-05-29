from sqlalchemy.orm import Session
from api.v1.repository import student_repository
from api.v1.schemas.student_schema import StudentCreate

def create_student(db: Session, student_data: StudentCreate):
    return student_repository.create_student(db, student_data)

def get_student_by_email(db: Session, email: str):
    return student_repository.get_student_by_email(db, email)

def list_students(db: Session):
    return student_repository.get_all_students(db)

def remove_student(db: Session, student_id: str):
    return student_repository.delete_student(db, student_id)