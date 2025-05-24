from fastapi import APIRouter, HTTPException, Path
from api.v1.schemas.project_schema import CompleteProjectInput, ProjectResponse, UpdateProjectInput
from api.v1.services.project_service import (
    delete_project_service,
    get_project_service,
    list_projects_service,
    list_user_projects,
    publish_project_service,
    update_project_service
)

router = APIRouter()

@router.get("/")
async def list_projects_route():
    try:
        return await list_projects_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/publish")
async def publish_project_route(payload: CompleteProjectInput):
    try:
        result = await publish_project_service(payload)
        return {"message": "Project published successfully!", "path": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_id}")
async def retrieve_project(project_id: int = Path(...)):
    try:
        return await get_project_service(project_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/projects/{project_id}")
async def update_project_route(project_id: int, payload: UpdateProjectInput):
    try:
        return await update_project_service(project_id, payload.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/projects/{project_id}")
async def delete_project_route(project_id: int):
    try:
        return await delete_project_service(project_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=list[ProjectResponse])
async def get_projects_by_user_id(user_id: str):
    try:
        projects = await list_user_projects(user_id)
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))