from sqlalchemy.orm import Session
from api.v1.schemas.student_schema import StudentCreate
from db.models.student import Student
import uuid

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