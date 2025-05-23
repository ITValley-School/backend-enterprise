from sqlalchemy import create_engine, text, inspect
import os
import logging
from db.base import Base
from db.session import engine
from db.models import *

def create_all_tables():
    Base.metadata.create_all(bind=engine)

def test_db_connection():
    try:
        with engine.connect() as conn:
            version = conn.execute(text("SELECT @@VERSION")).fetchone()
            logging.info(f"🧠 Conectado ao SQL Server: {version[0]}")

            inspector = inspect(engine)
            tables = inspector.get_table_names("tkse")
            logging.info(f"📦 Tabelas no schema 'tkse': {tables}")
    except Exception as e:
        logging.error(f"❌ Falha ao conectar ao banco: {e}")