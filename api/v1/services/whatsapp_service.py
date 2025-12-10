import os
import httpx
import logging
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class WhatsAppService:
    """
    Serviço para envio de mensagens via WhatsApp usando Evolution API
    """
    
    def __init__(self):
        self.evolution_api_url = os.getenv("EVOLUTION_API_URL", "https://app-evolutionapi-itvalley.azurewebsites.net")
        self.instance_name = os.getenv("EVOLUTION_API_INSTANCE_NAME", "itvalley")
        self.api_key = os.getenv("EVOLUTION_API_KEY", "")
        
        # Números de administradores que receberão notificações
        self.admin_numbers = [
            "48988312500",
            "17992379393", 
            "44999161570"
        ]
        
        if not self.api_key:
            logger.warning("EVOLUTION_API_KEY não configurada. Notificações WhatsApp podem falhar.")
    
    def _format_phone_number(self, number: str) -> str:
        """
        Formata o número de telefone para o formato esperado pela Evolution API
        Remove caracteres especiais e garante formato correto
        """
        # Remove caracteres não numéricos
        cleaned = ''.join(filter(str.isdigit, number))
        
        # Se começar com 55 (código do Brasil), mantém
        # Se não começar, assume que é número brasileiro e adiciona 55
        if cleaned.startswith('55'):
            return cleaned
        else:
            # Adiciona código do país 55 (Brasil)
            return f"55{cleaned}"
    
    def _get_headers(self) -> dict:
        """Retorna os headers necessários para as requisições"""
        headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }
        return headers
    
    async def send_message(
        self, 
        number: str, 
        message: str,
        instance_name: Optional[str] = None
    ) -> dict:
        """
        Envia uma mensagem de texto via WhatsApp usando Evolution API
        
        Args:
            number: Número de telefone do destinatário (formato: 5511999999999)
            message: Texto da mensagem a ser enviada
            instance_name: Nome da instância (opcional, usa a padrão se não fornecido)
            
        Returns:
            dict: Resposta da API
        """
        instance = instance_name or self.instance_name
        formatted_number = self._format_phone_number(number)
        
        url = f"{self.evolution_api_url}/message/sendText/{instance}"
        
        payload = {
            "number": formatted_number,
            "text": message
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._get_headers()
                )
                response.raise_for_status()
                
                result = response.json()
                logger.info(f"✅ Mensagem enviada para {formatted_number} via Evolution API")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ Erro HTTP ao enviar mensagem: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Erro ao enviar mensagem WhatsApp: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"❌ Erro de conexão ao enviar mensagem: {str(e)}")
            raise Exception(f"Erro de conexão com Evolution API: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao enviar mensagem: {str(e)}")
            raise
    
    async def send_notification_to_admins(
        self,
        student_name: str,
        project_name: str,
        deliverable_name: str,
        task_name: str,
        submission_id: str
    ) -> List[dict]:
        """
        Envia notificação para todos os administradores quando um entregável é submetido
        
        Args:
            student_name: Nome do estudante
            project_name: Nome do projeto
            deliverable_name: Nome do entregável
            task_name: Nome da tarefa
            submission_id: ID da submissão
            
        Returns:
            List[dict]: Lista com os resultados do envio para cada admin
        """
        message = self._format_submission_notification(
            student_name=student_name,
            project_name=project_name,
            deliverable_name=deliverable_name,
            task_name=task_name,
            submission_id=submission_id
        )
        
        results = []
        
        for admin_number in self.admin_numbers:
            try:
                result = await self.send_message(admin_number, message)
                results.append({
                    "number": admin_number,
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                logger.error(f"❌ Falha ao enviar notificação para {admin_number}: {str(e)}")
                results.append({
                    "number": admin_number,
                    "status": "error",
                    "error": str(e)
                })
        
        return results
    
    def _format_submission_notification(
        self,
        student_name: str,
        project_name: str,
        deliverable_name: str,
        task_name: str,
        submission_id: str
    ) -> str:
        """
        Formata a mensagem de notificação de submissão
        """
        message = f"""🚀 *Novo Entregável Submetido para Análise*

👤 *Estudante:* {student_name}
📁 *Projeto:* {project_name}
📦 *Entregável:* {deliverable_name}
✅ *Tarefa:* {task_name}
🆔 *ID da Submissão:* {submission_id}

⚠️ *Ação Necessária:* Esta submissão está aguardando validação.

Acesse o sistema para revisar e validar o entregável.
"""
        return message
    
    async def send_bulk_messages(
        self,
        numbers: List[str],
        message: str
    ) -> List[dict]:
        """
        Envia mensagem para múltiplos números
        
        Args:
            numbers: Lista de números de telefone
            message: Mensagem a ser enviada
            
        Returns:
            List[dict]: Lista com os resultados do envio
        """
        results = []
        
        for number in numbers:
            try:
                result = await self.send_message(number, message)
                results.append({
                    "number": number,
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                logger.error(f"❌ Falha ao enviar mensagem para {number}: {str(e)}")
                results.append({
                    "number": number,
                    "status": "error",
                    "error": str(e)
                })
        
        return results

