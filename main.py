from fastapi import FastAPI
from database.database import create_db_and_tables
from routers import directorRouter

async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(directorRouter.router)