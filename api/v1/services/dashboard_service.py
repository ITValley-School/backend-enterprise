from sqlalchemy.orm import Session
from uuid import UUID

from api.v1.repository.dashboard_repository import DashboardRepository


class DashboardService:
    @staticmethod
    def get_summary(db: Session, user_id: UUID):
        pending_tasks = DashboardRepository.count_pending_tasks(db, user_id)
        active_projects = DashboardRepository.count_active_projects(db, user_id)
        students_in_projects = DashboardRepository.count_students_in_projects(db, user_id)

        # Total geral
        total = pending_tasks + active_projects + students_in_projects or 1

        def percent(count):
            return f"{(count / total * 100):.1f}%"

        summary_cards = [
            {
                "title": "Total de Usuários",
                "count": students_in_projects,
                "percentage": percent(students_in_projects),
                "iconClass": "ri-user-line",
                "badgeClass": "success",
                "trendDirection": "up",
                "bgClass": "bg-primary-transparent",
            },
            {
                "title": "Projetos Ativos",
                "count": active_projects,
                "percentage": percent(active_projects),
                "iconClass": "ri-folder-line",
                "badgeClass": "success",
                "trendDirection": "up",
                "bgClass": "bg-secondary-transparent",
            },
            {
                "title": "Tarefas Pendentes",
                "count": pending_tasks,
                "percentage": percent(pending_tasks),
                "iconClass": "ri-task-line",
                "badgeClass": "warning",
                "trendDirection": "down",
                "bgClass": "bg-warning-transparent",
            },
        ]

        return summary_cards
