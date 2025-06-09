from uuid import UUID, uuid4
from fastapi import HTTPException, UploadFile
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from api.v1.repository.enterprise_repository import delete_enterprise, update_enterprise, create_enterprise
from api.v1.schemas.enterprise_schema import EnterpriseCreateForm, EnterpriseUpdate
from db.models.enterprise import Enterprise

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def update_enterprise_service(db: Session, enterprise_id: UUID, data: EnterpriseCreateForm):
    if data.profile_image:
        image_path = handle_image_upload(data.profile_image)
        data.profile_image_path = image_path
        
    if data.remove_image:
        data.profile_image_path = None
    
    if data.password:
        data.hashed_password = pwd_context.hash(data.password)
        
    enterprise = update_enterprise(db, enterprise_id, data)
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return enterprise


def delete_enterprise_service(db: Session, enterprise_id: UUID):
    success = delete_enterprise(db, enterprise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Enterprise not found")


def create_enterprise_service(data: EnterpriseCreateForm, db):

    hashed_password = pwd_context.hash(data.password)
    image_path = handle_image_upload(data.profile_image)

    db_enterprise = Enterprise(
    name=data.name,
    email=data.email,
    hashed_password=hashed_password,
    cnpj=data.cnpj,
    phone=data.phone,
    website=data.website,
    address=data.address,
    city=data.city,
    state=data.state,
    zip_code=data.zip_code,
    country_id=data.country_id,
    responsible_person=data.responsible_person,
    profile_image_path=image_path,
    )

    return create_enterprise(db, db_enterprise)


def handle_image_upload(image: UploadFile, base_path="static/uploads/enterprises/"):
    if not image:
        return None
    ext = image.filename.split(".")[-1]
    filename = f"{uuid4().hex}_{datetime.utcnow().timestamp()}.{ext}"
    os.makedirs(base_path, exist_ok=True)
    file_path = os.path.join(base_path, filename)
    with open(file_path, "wb") as f:
        f.write(image.file.read())
    return file_path