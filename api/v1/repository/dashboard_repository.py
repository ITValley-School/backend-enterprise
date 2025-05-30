from sqlalchemy.orm import Session
from uuid import UUID

from db.models.project import Project
from db.models.student_project import StudentProject
from db.models.task import Deliverable, Task



class DashboardRepository:
    @staticmethod
    def count_pending_tasks(db: Session, user_id: UUID) -> int:
        return (
            db.query(Task)
            .join(Deliverable, Task.deliverable_id == Deliverable.id)
            .join(Project, Deliverable.project_id == Project.id)
            .filter(Project.user_id == user_id, Task.status == "Pendente")
            .count()
        )

    @staticmethod
    def count_active_projects(db: Session, user_id: UUID):
        return (
            db.query(Project)
            .filter(Project.user_id == user_id, Project.status != "Finalizado")
            .count()
        )

    @staticmethod
    def count_students_in_projects(db: Session, user_id: UUID):
        return (
            db.query(StudentProject.student_id)
            .join(Project, Project.id == StudentProject.project_id)
            .filter(Project.user_id == user_id)
            .distinct()
            .count()
        )
