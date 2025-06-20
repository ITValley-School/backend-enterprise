from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from api.v1.services.dashboard_service import DashboardService
from db.models.project import Project
from db.models.task import Deliverable
from db.session import get_db


router = APIRouter()

@router.get("/summary/{enterprise_id}")
def get_dashboard_summary(enterprise_id: UUID, db: Session = Depends(get_db)):
    return DashboardService.get_summary(db, enterprise_id)

@router.get("/deliveries-per-project")
def get_deliveries_per_project(
    enterprise_id: str = Query(...),
    project_ids: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    current_year = datetime.now().year

    query = (
        db.query(
            Deliverable.project_id,
            Project.name.label("project_name"),
            func.month(Deliverable.created_at).label("month"),
            func.count(Deliverable.id).label("count")
        )
        .join(Project, Project.id == Deliverable.project_id)
        .filter(
            func.year(Deliverable.created_at) == current_year,
            Project.enterprise_id == enterprise_id,
            Deliverable.status == "COMPLETED"
        )
    )

    if project_ids:
        query = query.filter(Project.id.in_(project_ids))

    results = (
        query.group_by(
            Deliverable.project_id,
            Project.name,
            func.month(Deliverable.created_at)
        )
        .order_by(Project.name, func.month(Deliverable.created_at))
        .all()
    )

    # agrupa dados no formato ApexCharts
    project_data = {}
    for row in results:
        if row.project_name not in project_data:
            project_data[row.project_name] = [0] * 12
        project_data[row.project_name][row.month - 1] = row.count

    series = [
        {
            "name": project_name,
            "type": "line",
            "data": [
                {"x": datetime(1900, m + 1, 1).strftime('%b'), "y": monthly_data[m]}
                for m in range(12)
            ]
        }
        for project_name, monthly_data in project_data.items()
    ]

    return {"series": series}