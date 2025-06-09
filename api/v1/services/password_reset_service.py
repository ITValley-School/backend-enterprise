import secrets
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext

from db.models.password_reset import PasswordResetToken, UserType
from db.models.enterprise import Enterprise
from db.models.student import Student
from api.v1.services.email_service import EmailService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordResetService:
    
    @staticmethod
    def generate_reset_token(db: Session, email: str, user_type: str):
        """Gera token de recuperação e envia email"""
        
        # Validar tipo de usuário
        if user_type not in ["enterprise", "student"]:
            raise HTTPException(status_code=400, detail="Tipo de usuário inválido")
        
        # Buscar usuário
        user = None
        user_name = ""
        
        if user_type == "enterprise":
            user = db.query(Enterprise).filter(Enterprise.email == email).first()
            if user:
                user_name = user.name
        else:  # student
            user = db.query(Student).filter(Student.email == email, Student.is_active == True).first()
            if user:
                user_name = user.name
        
        if not user:
            # Por segurança, não revelamos se o email existe ou não
            raise HTTPException(status_code=404, detail="Email não encontrado")
        
        # Invalidar tokens anteriores deste usuário
        old_tokens = db.query(PasswordResetToken).filter(
            PasswordResetToken.email == email,
            PasswordResetToken.user_type == UserType(user_type),
            PasswordResetToken.is_used == "false"
        ).all()
        
        for token in old_tokens:
            token.is_used = "true"
        
        # Gerar novo token
        token_string = secrets.token_urlsafe(32)
        
        # Criar registro no banco
        reset_token = PasswordResetToken(
            token=token_string,
            email=email,
            user_type=UserType(user_type),
            user_id=str(user.id),
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
        )
        
        db.add(reset_token)
        db.commit()
        db.refresh(reset_token)
        
        # Enviar email
        try:
            email_service = EmailService()
            email_service.send_password_reset_email(
                to_email=email,
                token=token_string,
                user_name=user_name,
                user_type=user_type
            )
        except Exception as e:
            # Se falhar ao enviar email, remover token
            db.delete(reset_token)
            db.commit()
            raise HTTPException(status_code=500, detail="Erro ao enviar email de recuperação")
        
        return {
            "message": "Email de recuperação enviado com sucesso",
            "email": email
        }
    
    @staticmethod
    def reset_password(db: Session, token: str, new_password: str):
        """Reset da senha usando token"""
        
        # Buscar token
        reset_token = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.is_used == "false"
        ).first()
        
        if not reset_token:
            raise HTTPException(status_code=400, detail="Token inválido ou expirado")
        
        # Verificar se token não expirou
        if not reset_token.is_valid:
            raise HTTPException(status_code=400, detail="Token inválido ou expirado")
        
        # Buscar usuário
        user = None
        if reset_token.user_type == UserType.ENTERPRISE:
            user = db.query(Enterprise).filter(Enterprise.id == reset_token.user_id).first()
        else:  # STUDENT
            user = db.query(Student).filter(Student.id == reset_token.user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Atualizar senha
        hashed_password = pwd_context.hash(new_password)
        
        if reset_token.user_type == UserType.ENTERPRISE:
            user.hashed_password = hashed_password
        else:  # STUDENT
            user.password = hashed_password
        
        # Marcar token como usado
        reset_token.is_used = "true"
        
        db.commit()
        
        return {"message": "Senha alterada com sucesso"}
    
    @staticmethod
    def validate_token(db: Session, token: str):
        """Valida se um token é válido (para checagem no frontend)"""
        
        reset_token = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.is_used == "false"
        ).first()
        
        if not reset_token or not reset_token.is_valid:
            return {"valid": False, "message": "Token inválido ou expirado"}
        
        return {
            "valid": True, 
            "email": reset_token.email,
            "user_type": reset_token.user_type.value,
            "expires_at": reset_token.expires_at
        } 