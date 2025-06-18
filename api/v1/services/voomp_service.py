from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
import secrets
import string

from api.v1.schemas.voomp_schema import VoompWebhookPayload
from api.v1.schemas.student_schema import StudentCreate
from api.v1.services.student_service import create_student
from api.v1.services.password_reset_service import PasswordResetService
from api.v1.services.email_service import EmailService
from db.models.student import Student

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class VoompService:
    @staticmethod
    def process_webhook(payload: VoompWebhookPayload, db: Session):
        """Processa o webhook da Voomp"""
        
        # Verifica se é um evento de pagamento confirmado
        if payload.trigger != "salePaid" or payload.currentStatus != "paid":
            return {"message": "Evento ignorado - não é um pagamento confirmado"}
            
        # Verifica se o estudante já existe
        existing_student = db.query(Student).filter(
            Student.email == payload.client.email
        ).first()
        
        if existing_student:
            return {"message": "Estudante já existe", "student_id": existing_student.id}
            
        # Gera uma senha aleatória temporária
        temp_password = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(12)
        )
        
        # Cria o novo estudante
        student_data = StudentCreate(
            name=payload.client.name,
            email=payload.client.email,
            password=temp_password,  # Será alterada pelo usuário
            phone=payload.client.cellphone,
            role="introduction",  # Role padrão conforme solicitado
        )
        
        # Cria o estudante no banco
        new_student = create_student(db=db, student=student_data)
        
        # Gera token de redefinição de senha
        password_reset_service = PasswordResetService()
        reset_token = password_reset_service.generate_reset_token(
            db=db,
            email=payload.client.email,
            user_type="student"
        )
        
        # Envia email de boas-vindas com link para definir senha
        email_service = EmailService()
        email_service.send_welcome_email(
            to_email=payload.client.email,
            user_name=payload.client.name,
            token=reset_token["token"] if isinstance(reset_token, dict) else reset_token
        )
        
        return {
            "message": "Estudante criado com sucesso",
            "student_id": new_student.id
        } 