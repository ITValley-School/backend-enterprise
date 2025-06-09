from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.v1.schemas.auth_schema import EmailTestRequest
from api.v1.services.password_reset_service import PasswordResetService
from api.v1.services.email_service import EmailService
from db.session import get_db

router = APIRouter()

@router.get("/validate-reset-token")
def validate_reset_token(token: str = Query(...), db: Session = Depends(get_db)):
    """Valida se um token de recuperação é válido (para checagem no frontend)"""
    return PasswordResetService.validate_token(db, token)

@router.post("/send-test-email")
def send_test_email(data: EmailTestRequest):
    """Envia email de teste para verificar configuração"""
    try:
        email_service = EmailService()
        email_service.send_test_email(str(data.to_email), data.subject, data.message)
        return {"message": "Email de teste enviado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 