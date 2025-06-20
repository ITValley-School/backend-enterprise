from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from api.v1.repository.dashboard_repository import StudentDashboardRepository
from api.v1.repository.task_repository import TaskSubmissionRepository
from api.v1.schemas.task_schema import TaskSubmissionCreate, TaskSubmissionResponse, StudentSubmissionResponse
from api.v1.schemas.auth_schema import ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse
from api.v1.services import student_service
from api.v1.services.project_service import list_visible_projects
from db.session import get_db
from api.v1.schemas.student_schema import (
    StudentCreateForm,
    StudentDashboardResponse,
    StudentLoginRequest, 
    StudentTokenResponse, 
    StudentResponse,
    StudentUpdateForm, 
)
from api.v1.services.student_service import (
    create_access_token,
    create_student_service,
    list_deliverables_for_student, 
    verify_password, 
    list_students,
    get_student_by_id_service,
    update_student_service, 
    delete_student_service,
)
from api.v1.repository.student_repository import get_student_by_email, get_student_with_projects
from api.v1.services.password_reset_service import PasswordResetService

router = APIRouter()

@router.post("/login", response_model=StudentTokenResponse)
async def login(data: StudentLoginRequest, db: Session = Depends(get_db)):
    student = get_student_by_email(db, data.email)

    if not student or not verify_password(data.password, student.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = {"sub": str(student.id), "email": student.email}
    token = create_access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "phone": student.phone,
            "role": student.role,
            "location": student.location,
            "photo": student.photo,
            "cargo": student.cargo,
            "bio": student.bio,
            "github": student.github,
            "linkedin": student.linkedin,
            "welcome": student.welcome,
            "is_active": student.is_active,
            "created_at": student.created_at,
            "updated_at": student.updated_at
        }
    }

@router.post("/", response_model=StudentResponse)
def create_new_student(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    role: str = Form(...),
    location: str = Form(...),
    cargo: str = Form(...),
    bio: str = Form(...),
    github: str = Form(...),
    linkedin: str = Form(...),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    form_data = StudentCreateForm(
        name=name,
        email=email,
        password=password,
        phone=phone,
        role=role,
        location=location,
        cargo=cargo,
        bio=bio,
        github=github,
        linkedin=linkedin,
        profile_image=profile_image,
    )

    return create_student_service(form_data, db)

@router.get("/", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return list_students(db)

@router.get("/visible-projects")
def get_visible_projects(db: Session = Depends(get_db)):
    return list_visible_projects(db)

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: str, db: Session = Depends(get_db)):
    return get_student_by_id_service(db, student_id)

@router.get("/{student_id}/projects")
def get_student_projects(student_id: str, db: Session = Depends(get_db)):
    """Busca estudante com todos os seus projetos relacionados"""
    student = get_student_with_projects(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    projects = []
    for student_project in student.student_projects:
        project = student_project.project
        projects.append({
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "technologies": project.technologies,
            "complexity": project.complexity,
            "category": project.category,
            "score": project.score,
            "country": project.country,
            "joined_at": student_project.joined_at,
            "created_at": project.created_at
        })
    
    return {
        "student_id": student.id,
        "student_name": student.name,
        "projects": projects
    }

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: UUID,
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    cargo: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    github: Optional[str] = Form(None),
    linkedin: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    remove_image: Optional[bool] = Form(False),
    db: Session = Depends(get_db)
):
    form_data = StudentUpdateForm(
        name=name,
        email=email,
        password=password,
        phone=phone,
        role=role,
        location=location,
        cargo=cargo,
        bio=bio,
        github=github,
        linkedin=linkedin,
        profile_image=profile_image,
        remove_image=remove_image
    )

    return update_student_service(student_id, form_data, db)

@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    delete_student_service(db, student_id)

@router.get("/{student_id}/projects")
def get_projects_by_student(student_id: UUID, db: Session = Depends(get_db)):
    return student_service.get_projects_by_student(db, student_id)

@router.post("/{student_id}/projects/{project_id}")
def link_student_to_project(student_id: UUID, project_id: UUID, db: Session = Depends(get_db)):
    return student_service.link_student_to_project(db, student_id, project_id)

@router.get("/{student_id}/dashboard", response_model=StudentDashboardResponse)
def get_student_dashboard(student_id: UUID, db: Session = Depends(get_db)):
    try:
        data = StudentDashboardRepository.get_dashboard_data(db, student_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{student_id}/deliverables")
def get_student_deliverables(student_id: UUID, db: Session = Depends(get_db)):
    try:
        deliverables = list_deliverables_for_student(db, str(student_id))
        if deliverables is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return deliverables
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/{student_id}/submissions", response_model=TaskSubmissionResponse)
def submit_task(student_id: UUID, data: TaskSubmissionCreate, db: Session = Depends(get_db)):
    return TaskSubmissionRepository.create_submission(db, student_id, data)

@router.get("/{student_id}/submissions", response_model=List[StudentSubmissionResponse])
def get_student_submissions(student_id: UUID, db: Session = Depends(get_db)):
    """Busca todas as submissões de um estudante"""
    try:
        submissions = TaskSubmissionRepository.get_student_submissions(db, str(student_id))
        return submissions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Solicitação de recuperação de senha para estudantes"""
    return PasswordResetService.generate_reset_token(db, str(data.email), "student")

@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset de senha para estudantes usando token"""
    return PasswordResetService.reset_password(db, data.token, data.new_password)

@router.patch("/{student_id}/dismiss-welcome")
def dismiss_welcome(student_id: UUID, db: Session = Depends(get_db)):
    """Marca as boas-vindas como visualizadas (welcome = false)"""
    try:
        from api.v1.repository.student_repository import get_student_by_id, update_student
        from api.v1.schemas.student_schema import StudentUpdate
        
        # Verificar se estudante existe
        student = get_student_by_id(db, str(student_id))
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Atualizar welcome para false
        update_data = StudentUpdate(welcome=False)
        updated_student = update_student(db, str(student_id), update_data)
        
        return {
            "message": "Welcome dismissed successfully",
            "student_id": str(student_id),
            "welcome": False
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))