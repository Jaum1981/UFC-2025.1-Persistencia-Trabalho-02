from fastapi import FastAPI
from database import create_db_and_tables
from routers import directorRouter


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "oi"}

app.include_router(directorRouter.router)