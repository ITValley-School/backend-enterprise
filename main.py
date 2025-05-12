from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import setup_routes
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

setup_routes(app)


#Configurações de CORS
def get_cors_origins():
        origins = os.getenv('CORS_ORIGINS')
        if origins:
            return [origin.strip() for origin in origins.split(',')]
        return []


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)