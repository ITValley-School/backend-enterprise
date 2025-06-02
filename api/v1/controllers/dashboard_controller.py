from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.v1.services.dashboard_service import DashboardService
from db.session import get_db


router = APIRouter()

@router.get("/summary/{enterprise_id}")
def get_dashboard_summary(enterprise_id: UUID, db: Session = Depends(get_db)):
    return DashboardService.get_summary(db, enterprise_id)