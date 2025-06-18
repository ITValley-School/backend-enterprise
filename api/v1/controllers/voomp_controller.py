from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.session import get_db
from api.v1.schemas.voomp_schema import VoompWebhookPayload
from api.v1.services.voomp_service import VoompService
import logging

# Configurar logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/webhook")
async def voomp_webhook(request: Request, db: Session = Depends(get_db)):
    """Endpoint para receber webhooks da Voomp"""
    try:
        # Log do payload recebido
        payload = await request.json()
        logger.info(f"📩 Payload recebido da Voomp: {payload}")
        
        # Validar e processar o payload
        voomp_payload = VoompWebhookPayload(**payload)
        
        # Processar o webhook
        voomp_service = VoompService()
        result = voomp_service.process_webhook(voomp_payload, db)
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar webhook da Voomp: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar webhook: {str(e)}"
        ) 