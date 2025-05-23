from fastapi import FastAPI
from api.v1.controllers import agent_project_deliver_controller
from api.v1.controllers import project_controller



def setup_routes(app: FastAPI) -> None:
    """
    Setup the routes for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(agent_project_deliver_controller.router, prefix="/api/agent", tags=["agent"])
    app.include_router(project_controller.router, prefix="/api/projects", tags=["projects"])