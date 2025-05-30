from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.v1.services.dashboard_service import DashboardService
from db.session import get_db


router = APIRouter()

@router.get("/summary/{user_id}")
def get_dashboard_summary(user_id: UUID, db: Session = Depends(get_db)):
    return DashboardService.get_summary(db, user_id)