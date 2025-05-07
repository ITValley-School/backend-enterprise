from fastapi import FastAPI
#from api.routes import auth, users, posts, comments
from api.controllers import agentProjectDeliverController



def setup_routes(app: FastAPI) -> None:
    """
    Setup the routes for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """


    #app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    #app.include_router(users.router, prefix="/api/users", tags=["users"])
    #app.include_router(posts.router, prefix="/appi/posts", tags=["posts"])
    #app.include_router(comments.router, prefix="/api/comments", tags=["comments"])
    app.include_router(agentProjectDeliverController.router, prefix="/api/agent", tags=["agent"])