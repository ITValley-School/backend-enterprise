from uuid import UUID
from fastapi import APIRouter, HTTPException
from api.v1.schemas.user_schema import LoginRequest, TokenResponse, UserCreate, UserResponse, UserUpdate
from api.v1.services.user_service import create_access_token, verify_password, update_user_service, delete_user_service
from api.v1.repository.user_repository import create_user, get_user_by_email, get_user_by_id, get_user_by_username

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    user = get_user_by_username(data.username)
    
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token_data = {"sub": str(user.id), "username": user.username}
    token = create_access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email
        }
    }

@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate):
    db_user = get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: UUID):
    db_user = get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, data: UserUpdate):
    return update_user_service(user_id, data)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID):
    delete_user_service(user_id)