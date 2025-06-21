from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from api.v1.controllers import agent_project_deliver_controller, chat_ws_controller, enterprise_controller, project_controller, student_controller, dashboard_controller, country_controller, auth_controller, student_project_controller, voomp_controller



def setup_routes(app: FastAPI) -> None:
    """
    Setup the routes for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    api_router = APIRouter(prefix="/api")

    # Rotas de autenticação
    api_router.include_router(auth_controller.router, prefix="/auth", tags=["auth"])

    # Rotas de empresas
    api_router.include_router(enterprise_controller.router, prefix="/enterprises", tags=["enterprises"])

    # Rotas de estudantes
    api_router.include_router(student_controller.router, prefix="/students", tags=["students"])

    # Rotas de projetos
    api_router.include_router(project_controller.router, prefix="/projects", tags=["projects"])

    # Rotas de vínculo estudante-projeto
    api_router.include_router(student_project_controller.router, prefix="/student-projects", tags=["student-projects"])

    # Rotas de países
    api_router.include_router(country_controller.router, prefix="/countries", tags=["countries"])

    # Rotas de dashboard
    api_router.include_router(dashboard_controller.router, prefix="/dashboard", tags=["dashboard"])

    # Rotas de entrega de projetos
    api_router.include_router(agent_project_deliver_controller.router, prefix="/agent-project-deliver", tags=["agent-project-deliver"])

    # Rotas de webhook da Voomp
    api_router.include_router(voomp_controller.router, prefix="/voomp", tags=["voomp"])
    
    api_router.include_router(chat_ws_controller.router, prefix="/chat", tags=["chat"])

    app.include_router(api_router)
    app.mount("/static", StaticFiles(directory="static"), name="static")