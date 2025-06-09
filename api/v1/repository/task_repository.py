from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException
from requests import Session

from api.v1.schemas.task_schema import TaskSubmissionCreate, TaskSubmissionValidate
from db.models.enterprise import Enterprise
from db.models.student import Student
from db.models.task import Task, TaskSubmission


class TaskSubmissionRepository:
    @staticmethod
    def create_submission(db: Session, student_id: str, data: TaskSubmissionCreate):
        try:
            task_id = str(UUID(str(data.task_id)))
            student_id = str(UUID(str(student_id)))
        except ValueError:
            raise HTTPException(status_code=400, detail="UUID inválido")

        task_exists = db.query(Task).filter(Task.id == task_id).first()
        if not task_exists:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

        student_exists = db.query(Student).filter(Student.id == student_id).first()
        if not student_exists:
            raise HTTPException(status_code=404, detail="Aluno não encontrado.")

        submission = TaskSubmission(
            task_id=task_id,
            student_id=student_id,
            submission_link=data.submission_link,
            branch_name=data.branch_name,
            evidence_file=data.evidence_file
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def validate_submission(db: Session, submission_id: UUID, data: TaskSubmissionValidate):
        
        enterprise = db.query(Enterprise).filter(Enterprise.id == data.validator_id).first()
        if not enterprise:
            raise HTTPException(status_code=404, detail="Empresa validadora não encontrada")

        submission = db.query(TaskSubmission).filter(TaskSubmission.id == str(submission_id)).first()
        if not submission:
            raise HTTPException(status_code=404, detail="Submissão não encontrada.")

        if data.status not in ("APPROVED", "REJECTED"):
            raise HTTPException(status_code=400, detail="Status inválido. Use 'APPROVED' ou 'REJECTED'.")

        submission.status = data.status
        submission.feedback = data.feedback
        submission.validated_by = str(data.validator_id)
        submission.validated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(submission)
        return submission