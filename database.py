from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os


load_dotenv("db.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session() -> Session:
    return Session(engine)