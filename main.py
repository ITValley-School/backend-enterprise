from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import os

from api.v1.routes import setup_routes
from db.init_db import test_db_connection, create_all_tables

# Carrega variáveis de ambiente
load_dotenv()

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("azure").setLevel(logging.WARNING)

# Inicializa FastAPI
app = FastAPI()

create_all_tables()

# Testa conexão com banco
test_db_connection()

# Registra rotas
setup_routes(app)

# Configura CORS
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
