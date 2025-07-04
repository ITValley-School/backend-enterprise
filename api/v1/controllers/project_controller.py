from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from db.session import get_db
from api.v1.schemas.project_schema import CompleteProjectInput, ProjectBasicInfo, ProjectList, ProjectResponse, UpdateProjectInput, UpdateStatusInput
from api.v1.services.project_service import (
    delete_project_service,
    get_filtered_projects,
    get_project_service,
    list_enterprise_projects,
    list_projects_service,
    publish_project_service,
    update_project_service,
    update_project_status_service,
    list_projects_by_enterprise_service
)

router = APIRouter()

@router.get("/", response_model=list[ProjectList])
async def list_projects_route(db: Session = Depends(get_db)):
    try:
        return await list_projects_service(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/projects-options", response_model=List[ProjectBasicInfo])
async def list_projects(
    enterprise_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    return await list_projects_by_enterprise_service(db, enterprise_id)

    
@router.post("/publish")
async def publish_project_route(payload: CompleteProjectInput, db: Session = Depends(get_db)):
    try:
        result = await publish_project_service(db, payload)
        return {"message": "Project published successfully!", "path": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/filter", response_model=list[ProjectResponse])
def filter_projects(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return get_filtered_projects(db, name)
    
@router.get("/{project_id}")
async def retrieve_project(project_id: UUID, db: Session = Depends(get_db)):
    try:
        return await get_project_service(db, project_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{project_id}")
async def update_project_route(project_id: UUID, payload: UpdateProjectInput, db: Session = Depends(get_db)):
    try:
        return await update_project_service(db, project_id, payload.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{project_id}")
async def delete_project_route(project_id: UUID, db: Session = Depends(get_db)):
    try:
        return await delete_project_service(db, project_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/enterprises/{enterprise_id}", response_model=list[ProjectResponse])
async def get_projects_by_enterprise_id(enterprise_id: UUID, db: Session = Depends(get_db)):
    try:
        projects = await list_enterprise_projects(db, enterprise_id)
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/{project_id}/status")
async def update_project_status_route(
    project_id: UUID,
    payload: UpdateStatusInput,
    db: Session = Depends(get_db)
):
    try:
        updated = await update_project_status_service(db, str(project_id), payload.new_status)
        return {"message": f"Status atualizado para {payload.new_status}", "project": updated}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
