import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_PORT", "587"))
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")
        
        if not self.username or not self.password:
            raise ValueError("Email credentials not configured. Please set EMAIL_USERNAME and EMAIL_PASSWORD in .env file")

    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None):
        """Envia email com conteúdo HTML e texto alternativo"""
        try:
            # Criar mensagem
            msg = MIMEMultipart("alternative")
            msg["From"] = self.username
            msg["To"] = to_email
            msg["Subject"] = subject

            # Adicionar versão texto se fornecida
            if text_content:
                text_part = MIMEText(text_content, "plain")
                msg.attach(text_part)

            # Adicionar versão HTML
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            # Configurar conexão SMTP
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.send_message(msg)
                
            return True
            
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao enviar email: {str(e)}")

    def send_password_reset_email(self, to_email: str, token: str, user_name: str, user_type: str):
        """Envia email de recuperação de senha"""
        
        # URL base do frontend - você pode configurar no .env
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        reset_url = f"{frontend_url}/reset-password?token={token}&type={user_type}"
        
        subject = "Recuperação de Senha - Backend Enterprise"
        
        # Versão HTML do email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background-color: #f8f9fa; }}
                .button {{ background-color: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
                .footer {{ padding: 20px; text-align: center; color: #666; font-size: 12px; }}
                .warning {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Recuperação de Senha</h1>
                </div>
                
                <div class="content">
                    <h2>Olá, {user_name}!</h2>
                    <p>Recebemos uma solicitação para redefinir a senha da sua conta.</p>
                    
                    <p>Clique no botão abaixo para criar uma nova senha:</p>
                    
                    <p style="text-align: center;">
                        <a href="{reset_url}" class="button">🔑 Redefinir Senha</a>
                    </p>
                    
                    <div class="warning">
                        <strong>⏰ Importante:</strong> Este link é válido por apenas 1 hora por motivos de segurança.
                    </div>
                    
                    <p>Se você não solicitou a redefinição de senha, pode ignorar este email. Sua senha permanecerá inalterada.</p>
                    
                    <p><strong>Link alternativo:</strong><br>
                    <small>{reset_url}</small></p>
                </div>
                
                <div class="footer">
                    <p>Este é um email automático, não responda.</p>
                    <p>© 2024 Backend Enterprise. Todos os direitos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Versão texto alternativa
        text_content = f"""
        Recuperação de Senha - Backend Enterprise
        
        Olá, {user_name}!
        
        Recebemos uma solicitação para redefinir a senha da sua conta.
        
        Acesse o link abaixo para criar uma nova senha:
        {reset_url}
        
        IMPORTANTE: Este link é válido por apenas 1 hora por motivos de segurança.
        
        Se você não solicitou a redefinição de senha, pode ignorar este email.
        
        ---
        Este é um email automático, não responda.
        © 2024 Backend Enterprise
        """
        
        return self.send_email(to_email, subject, html_content, text_content)

    def send_test_email(self, to_email: str, subject: str, message: str):
        """Envia email de teste"""
        html_content = f"""
        <html>
        <body>
            <h2>Email de Teste</h2>
            <p>{message}</p>
            <p><small>Enviado em: {os.getenv('EMAIL_USERNAME')}</small></p>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content, message) 