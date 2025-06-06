from fastapi import FastAPI
from database import create_db_and_tables
from routers import directorRouter

import models.movie            
import models.director         
import models.movie_director_link
import models.session
import models.room
import models.ticket


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "oi"}

app.include_router(directorRouter.router)