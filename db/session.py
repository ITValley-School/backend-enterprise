import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

AZURE_SQL_CONNECTION_STRING = os.getenv("AZURE_SQL_CONNECTION_STRING")

if not AZURE_SQL_CONNECTION_STRING:
    raise ValueError(
        "AZURE_SQL_CONNECTION_STRING environment variable is not set. "
        "Please configure this variable in your Azure App Service settings."
    )

engine = create_engine(AZURE_SQL_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()