from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import UUID

from db.models.project import Project
from db.models.student_project import StudentProject
from db.models.task import Deliverable, Task



class DashboardRepository:
    @staticmethod
    def count_pending_tasks(db: Session, enterprise_id: UUID) -> int:
        return (
            db.query(Task)
            .join(Deliverable, Task.deliverable_id == Deliverable.id)
            .join(Project, Deliverable.project_id == Project.id)
            .filter(Project.enterprise_id == enterprise_id, Project.status != "PENDING", Task.status == "Pendente")
            .count()
        )

    @staticmethod
    def count_active_projects(db: Session, enterprise_id: UUID):
        return (
            db.query(Project)
            .filter(Project.enterprise_id == enterprise_id, Project.status != "COMPLETED", Project.status != "CANCELLED", Project.status != "PENDING")
            .count()
        )

    @staticmethod
    def count_students_in_projects(db: Session, enterprise_id: UUID):
        return (
            db.query(StudentProject.student_id)
            .join(Project, Project.id == StudentProject.project_id)
            .filter(Project.enterprise_id == enterprise_id, Project.status != "COMPLETED", Project.status != "CANCELLED", Project.status != "PENDING")
            .distinct()
            .count()
        )

class StudentDashboardRepository:

    @staticmethod
    def get_dashboard_data(db: Session, student_id: UUID):
        # Subquery para pegar projetos do aluno
        student_projects = (
            db.query(StudentProject.project_id)
            .filter(StudentProject.student_id == student_id)
            .subquery()
        )

        # Total de entregáveis
        total_deliverables = (
            db.query(Deliverable)
            .join(Project, Deliverable.project_id == Project.id)
            .filter(Deliverable.project_id.in_(student_projects))
            .count()
        )

        # Total de tarefas por status
        tasks_query = (
            db.query(Task.status, func.count(Task.id))
            .join(Deliverable, Task.deliverable_id == Deliverable.id)
            .join(Project, Deliverable.project_id == Project.id)
            .filter(Project.id.in_(student_projects))
            .group_by(Task.status)
            .all()
        )

        # Processa os dados de status
        completed_tasks = 0
        in_progress_tasks = 0

        for status, count in tasks_query:
            if status == "Concluída":
                completed_tasks = count
            else:
                in_progress_tasks += count

        return {
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "total_deliverables": total_deliverables,
            "certificate": 0
        }
