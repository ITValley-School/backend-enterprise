from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import setup_routes

app = FastAPI()

setup_routes(app)