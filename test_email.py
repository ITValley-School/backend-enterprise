import os
from dotenv import load_dotenv
import smtplib
import ssl
from email.mime.text import MIMEText

load_dotenv()

def test_email_config():
    """Testa configuração de email"""
    
    print("🔍 Verificando configurações de email...")
    
    # Carregar variáveis
    smtp_server = os.getenv("EMAIL_HOST")
    smtp_port = int(os.getenv("EMAIL_PORT", "587"))
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    
    print(f"📧 SMTP Server: {smtp_server}")
    print(f"🔌 SMTP Port: {smtp_port}")
    print(f"👤 Username: {username}")
    print(f"🔐 Password: {'*' * len(password) if password else 'NÃO CONFIGURADA'}")
    
    if not username or not password:
        print("❌ ERRO: EMAIL_USERNAME ou EMAIL_PASSWORD não configurados no .env")
        return False
    
    print("\n🚀 Testando conexão SMTP...")
    
    try:
        # Testar conexão
        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            print("✅ Conectado ao servidor SMTP")
            
            server.starttls(context=context)
            print("✅ TLS habilitado")
            
            server.login(username, password)
            print("✅ Login realizado com sucesso!")
            
            print("🎉 Configuração de email está funcionando!")
            return True
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ ERRO DE AUTENTICAÇÃO: {e}")
        print("\n💡 DICAS PARA RESOLVER:")
        print("1. Verifique se está usando uma SENHA DE APP (não a senha normal do Gmail)")
        print("2. Ative a autenticação de 2 fatores no Gmail")
        print("3. Gere uma senha de app em: https://myaccount.google.com/apppasswords")
        print("4. Use a senha de app gerada no EMAIL_PASSWORD")
        return False
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        return False

def send_test_email():
    """Envia email de teste"""
    
    if not test_email_config():
        return
    
    username = os.getenv("EMAIL_USERNAME")
    
    print(f"\n📤 Enviando email de teste para {username}...")
    
    try:
        from api.v1.services.email_service import EmailService
        
        email_service = EmailService()
        email_service.send_test_email(
            to_email=username,  # Envia para o próprio email
            subject="🧪 Teste de Configuração de Email",
            message="Se você recebeu este email, a configuração está funcionando perfeitamente! 🎉"
        )
        
        print("✅ Email de teste enviado com sucesso!")
        print(f"📬 Verifique sua caixa de entrada: {username}")
        
    except Exception as e:
        print(f"❌ Erro ao enviar email de teste: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 DIAGNÓSTICO DE CONFIGURAÇÃO DE EMAIL")
    print("=" * 50)
    
    send_test_email()
    
    print("\n" + "=" * 50)
    print("📋 CHECKLIST PARA GMAIL:")
    print("✓ Ativar autenticação de 2 fatores")
    print("✓ Gerar senha de app em: https://myaccount.google.com/apppasswords")
    print("✓ Usar a senha de app (não a senha normal)")
    print("✓ Verificar se EMAIL_USERNAME e EMAIL_PASSWORD estão no .env")
    print("=" * 50) 