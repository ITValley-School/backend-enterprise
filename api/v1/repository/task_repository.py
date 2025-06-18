from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException
from requests import Session
from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload

from api.v1.schemas.project_schema import ProjectResponse
from api.v1.schemas.task_schema import DeliverableWithTasks, ProjectResponseSchema, SubmissionWithDeliverable, TaskBasicInfo, TaskSubmissionCreate, TaskSubmissionValidate
from db.models.enterprise import Enterprise
from db.models.project import Project
from db.models.student import Student
from db.models.task import Deliverable, Task, TaskSubmission


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
        submission.task.status = submission.status
        submission.validated_by = str(data.validator_id)
        submission.validated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def get_student_submissions(db: Session, student_id: str):
        """Busca todas as submissões de um estudante com informações da task e validator"""
        try:
            student_uuid = str(UUID(str(student_id)))
        except ValueError:
            raise HTTPException(status_code=400, detail="UUID do estudante inválido")

        # Verifica se o estudante existe
        student_exists = db.query(Student).filter(Student.id == student_uuid).first()
        if not student_exists:
            raise HTTPException(status_code=404, detail="Estudante não encontrado")

        # Busca todas as submissões do estudante com joins
        submissions = db.query(TaskSubmission).options(
            joinedload(TaskSubmission.task),
            joinedload(TaskSubmission.validator)
        ).filter(TaskSubmission.student_id == student_uuid).order_by(TaskSubmission.submitted_at.desc()).all()

        return submissions
    
    @staticmethod
    def get_submissions_grouped_by_deliverable(db: Session, enterprise_id: UUID) -> List[SubmissionWithDeliverable]:
        submissions = (
            db.query(TaskSubmission)
            .join(Task)
            .join(Deliverable)
            .join(Project)
            .filter(Project.enterprise_id == enterprise_id)
            .order_by(TaskSubmission.submitted_at.desc())
            .all()
        )

        results = []
        for submission in submissions:
            deliverable = submission.task.deliverable
            project = deliverable.project

            if not deliverable or not project:
                continue

            deliverable_with_project = DeliverableWithTasks(
                id=deliverable.id,
                name=deliverable.name,
                status=deliverable.status,
                tasks=[TaskBasicInfo.from_orm(t) for t in deliverable.tasks],
                project=ProjectResponseSchema.from_orm(deliverable.project)
            )

            results.append(SubmissionWithDeliverable(
                id=submission.id,
                task_id=submission.task.id,
                status=submission.status,
                submission_link=submission.submission_link,
                branch_name=submission.branch_name,
                evidence_file=submission.evidence_file,
                feedback=submission.feedback,
                submitted_at=submission.submitted_at,
                validated_at=submission.validated_at,
                validator=submission.validator,
                student=submission.student,
                deliverable=deliverable_with_project
            ))

        return results

    @staticmethod
    def get_filtered_submissions_to_validate(
        db: Session,
        enterprise_id: UUID,
        search: Optional[str] = None,
        project_id: Optional[UUID] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[SubmissionWithDeliverable]:

        query = (
            db.query(TaskSubmission)
            .options(
                joinedload(TaskSubmission.task)
                    .joinedload(Task.deliverable)
                    .joinedload(Deliverable.project),
                joinedload(TaskSubmission.task)
                    .joinedload(Task.deliverable)
                    .joinedload(Deliverable.tasks),
                joinedload(TaskSubmission.student),
                joinedload(TaskSubmission.validator)
            )
            .join(Task)
            .join(Deliverable)
            .join(Project)
            .join(Student)
            .filter(Project.enterprise_id == enterprise_id)
        )

        if search:
            search_like = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Student.name).like(search_like),
                    func.lower(Deliverable.name).like(search_like),
                    func.lower(Task.name).like(search_like),
                )
            )

        if project_id:
            query = query.filter(Project.id == project_id)

        if status:
            query = query.filter(TaskSubmission.status == status)

        query = query.order_by(TaskSubmission.submitted_at.desc())
        submissions = query.limit(limit).offset(offset).all()

        results = []
        for submission in submissions:
            deliverable = submission.task.deliverable
            project = deliverable.project if deliverable else None
            if not deliverable or not project:
                continue

            deliverable_with_project = DeliverableWithTasks(
                id=deliverable.id,
                name=deliverable.name,
                status=deliverable.status,
                project=ProjectResponse.from_orm(project),
                tasks=[TaskBasicInfo.from_orm(task) for task in deliverable.tasks]
            )

            results.append(SubmissionWithDeliverable(
                id=submission.id,
                task_id=submission.task.id,
                status=submission.status,
                submission_link=submission.submission_link,
                branch_name=submission.branch_name,
                evidence_file=submission.evidence_file,
                feedback=submission.feedback,
                submitted_at=submission.submitted_at,
                validated_at=submission.validated_at,
                validator=submission.validator,
                student=submission.student,
                deliverable=deliverable_with_project
            ))

        return results