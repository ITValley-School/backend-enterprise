"""
Serviço para enviar notificações quando uma submissão é criada
"""
import logging
from sqlalchemy.orm import Session
from db.models.task import Deliverable, Task
from db.models.student import Student

logger = logging.getLogger(__name__)


async def send_submission_notification(
    db: Session,
    submission_id: str,
    student_id: str,
    task_id: str
):
    """
    Envia notificação WhatsApp para administradores quando uma submissão é criada
    
    Args:
        db: Sessão do banco de dados
        submission_id: ID da submissão criada
        student_id: ID do estudante
        task_id: ID da tarefa
    """
    try:
        # Busca informações necessárias usando joins para otimizar
        from sqlalchemy.orm import joinedload
        
        task = db.query(Task).options(
            joinedload(Task.deliverable).joinedload(Deliverable.project)
        ).filter(Task.id == task_id).first()
        
        if not task:
            logger.warning(f"Tarefa não encontrada: {task_id}")
            return
        
        deliverable = task.deliverable
        if not deliverable:
            logger.warning(f"Deliverable não encontrado para task {task_id}")
            return
        
        project = deliverable.project
        if not project:
            logger.warning(f"Projeto não encontrado para deliverable {deliverable.id}")
            return
        
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            logger.warning(f"Estudante não encontrado: {student_id}")
            return
        
        # Importa e envia notificação
        from api.v1.services.whatsapp_service import WhatsAppService
        whatsapp_service = WhatsAppService()
        
        await whatsapp_service.send_notification_to_admins(
            student_name=student.name,
            project_name=project.name,
            deliverable_name=deliverable.name,
            task_name=task.name,
            submission_id=submission_id
        )
        
        logger.info(f"✅ Notificação WhatsApp enviada para admins sobre submissão {submission_id}")
        
    except Exception as e:
        # Log do erro mas não falha o processo
        logger.error(f"❌ Erro ao enviar notificação WhatsApp: {str(e)}", exc_info=True)

