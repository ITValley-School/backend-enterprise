import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from agents import function_tool
import os
from dotenv import load_dotenv

load_dotenv()


class AgentTools:
    """Classe contendo todas as ferramentas disponíveis para os agentes"""
    
    @staticmethod
    def get_agent_capabilities():

        """Retorna o catálogo de capacidades do agente diretamente"""
        return {
            "email": "Posso enviar e-mails via API quando solicitado",
            "contacts": "Posso acessar um catálogo de endereços com e-mails salvos. Basta informar o nome da pessoa",
            "conversation": "Posso conversar amigavelmente e ajudar com suas dúvidas"
        }

    @staticmethod
    def get_email_catalog():
        """Retorna o catálogo de contatos diretamente na classe de ferramentas"""
        return {
            "carlos viana": "carlosaraujoviana@gmail.com",
            "carlos santana": "carlossantana@gmail.com",
            "julia robert": "julia@robert.com"
        }
    
    @staticmethod
    @function_tool
    def listar_capacidades():
        """Lista todas as capacidades que o agente possui"""
        capabilities = AgentTools.get_agent_capabilities()
        return {
            "capacidades": "\n".join([f"{i+1}. {val}" for i, val in enumerate(capabilities.values())])
        }
    
    @staticmethod
    @function_tool
    def buscar_capacidade(tipo: str):
        """
        Busca informações sobre uma capacidade específica
        
        Args:
            tipo: Tipo de capacidade (email, contacts, conversation)
        """
        capabilities = AgentTools.get_agent_capabilities()
        if tipo.lower() in capabilities:
            return {"detalhes": capabilities[tipo.lower()]}
        else:
            return {"detalhes": f"Capacidade '{tipo}' não encontrada. Capacidades disponíveis: {', '.join(capabilities.keys())}"}
    
    @staticmethod
    @function_tool
    def listar_contatos():
        """Lista todos os contatos disponíveis no catálogo"""
        catalog = AgentTools.get_email_catalog()
        contatos_formatados = []
        
        for nome, email in catalog.items():
            nome_formatado = ' '.join(word.capitalize() for word in nome.split())
            contatos_formatados.append(f"{nome_formatado}: {email}")
        
        return {
            "contatos": "\n".join(contatos_formatados)
        }
    
    @staticmethod
    @function_tool
    def buscar_email(nome: str):
        """
        Busca o email de um contato pelo nome
        
        Args:
            nome: Nome do contato a ser buscado
        """
        catalog = AgentTools.get_email_catalog()
        nome_lower = nome.lower()
        
        # Busca exata
        if nome_lower in catalog:
            return {"email": catalog[nome_lower], "nome": nome}
        
        # Busca parcial
        possiveis_contatos = []
        for contato in catalog.keys():
            if nome_lower in contato:
                nome_formatado = ' '.join(word.capitalize() for word in contato.split())
                possiveis_contatos.append(f"{nome_formatado}: {catalog[contato]}")
        
        if possiveis_contatos:
            return {
                "mensagem": f"Encontrei {len(possiveis_contatos)} contato(s) que correspondem a '{nome}':",
                "contatos": "\n".join(possiveis_contatos)
            }
        else:
            return {"mensagem": f"Não encontrei nenhum contato com o nome '{nome}' no catálogo."}
    
    @staticmethod
    @function_tool
    def enviar_email(destinatario: str, assunto: str, conteudo: str):
        """
        Envia um email para o destinatário especificado
        
        Args:
            destinatario: Endereço de email do destinatário
            assunto: Assunto do email
            conteudo: Corpo do email
        """
        try:
            # Configurações para envio de email usando Gmail
            remetente = "carlosaraujoviana@gmail.com"
            senha_app = os.environ.get("EMAIL_APP_PASSWORD")  # Use uma senha de aplicativo
            
            # Se não há senha configurada, retorna erro
            if not senha_app:
                return {
                    "status": "erro", 
                    "mensagem": "Senha de aplicativo do Gmail não configurada. Configure a variável de ambiente EMAIL_APP_PASSWORD."
                }
                
            # Cria a mensagem
            mensagem = MIMEMultipart()
            mensagem["From"] = remetente
            mensagem["To"] = destinatario
            mensagem["Subject"] = assunto
            
            # Adiciona o corpo do email
            mensagem.attach(MIMEText(conteudo, "plain"))
            
            # Conecta ao servidor SMTP do Gmail
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
                servidor.login(remetente, senha_app)
                servidor.send_message(mensagem)
            
            # Retorna sucesso
            return {
                "status": "sucesso",
                "mensagem": f"Email enviado com sucesso para {destinatario}",
                "detalhes": {
                    "destinatario": destinatario,
                    "assunto": assunto,
                    "horario_envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro ao enviar email: {str(e)}"
            }
    
    @staticmethod
    @function_tool
    def validar_email(endereco_email: str):
        """
        Valida se um endereço de email está em formato correto
        
        Args:
            endereco_email: Endereço de email para validar
        """
        import re
        
        # Padrão básico de validação de email
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        if re.match(padrao, endereco_email):
            return {"valido": True}
        else:
            return {"valido": False, "mensagem": "O formato do email não parece válido."}

