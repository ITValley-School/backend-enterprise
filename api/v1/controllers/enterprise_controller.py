from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.v1.repository.task_repository import TaskSubmissionRepository
from api.v1.schemas.task_schema import TaskSubmissionResponse, TaskSubmissionValidate
from db.session import get_db
from api.v1.schemas.enterprise_schema import (
    EnterpriseCreateForm,
    LoginRequest,
    TokenResponse,
    EnterpriseResponse,
    EnterpriseUpdate
)
from api.v1.services.enterprise_service import (
    create_access_token,
    create_enterprise_service,
    verify_password,
    update_enterprise_service,
    delete_enterprise_service
)
from api.v1.repository.enterprise_repository import (
    get_enterprise_by_email,
    get_enterprise_by_id,
)

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    enterprise = get_enterprise_by_email(db, data.email)

    if not enterprise or not verify_password(data.password, enterprise.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token_data = {"sub": str(enterprise.id), "email": enterprise.email}
    token = create_access_token(token_data)

    user_data = enterprise.__dict__.copy()
    user_data.pop("hashed_password", None)
    user_data.pop("password", None)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_data
    }


@router.post("/", response_model=EnterpriseResponse)
def create_new_enterprise(data: EnterpriseCreateForm = Depends(), db: Session = Depends(get_db)):
    return create_enterprise_service(data, db)


@router.get("/{enterprise_id}", response_model=EnterpriseResponse)
def read_enterprise(enterprise_id: UUID, db: Session = Depends(get_db)):
    enterprise = get_enterprise_by_id(db, enterprise_id)
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return EnterpriseResponse.model_validate(enterprise)


@router.put("/{enterprise_id}", response_model=EnterpriseResponse)
def update_enterprise(enterprise_id: UUID, data: EnterpriseCreateForm = Depends(), db: Session = Depends(get_db)):
    return update_enterprise_service(db, enterprise_id, data)


@router.delete("/{enterprise_id}", status_code=204)
def delete_enterprise(enterprise_id: UUID, db: Session = Depends(get_db)):
    delete_enterprise_service(db, enterprise_id)


@router.post("/submissions/{submission_id}/validate", response_model=TaskSubmissionResponse)
def validate_task_submission(
    submission_id: UUID,
    data: TaskSubmissionValidate,
    db: Session = Depends(get_db),
):
    return TaskSubmissionRepository.validate_submission(db, submission_id, data)