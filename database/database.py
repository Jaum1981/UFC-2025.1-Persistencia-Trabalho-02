from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import event
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "db.env"))

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# Ativa a verificação de foreign keys no SQLite
from sqlalchemy.engine import Engine
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session() -> Session:
    return Session(engine)