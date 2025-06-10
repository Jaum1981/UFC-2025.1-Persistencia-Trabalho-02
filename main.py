from fastapi import FastAPI
from database.database import create_db_and_tables
from routers import director_router, movie_router, room_router, session_router, payment_router, ticket_router, complex_router


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "oi"}

app.include_router(director_router.router)
app.include_router(movie_router.router)
app.include_router(room_router.router)
app.include_router(session_router.router)
app.include_router(payment_router.router)
app.include_router(ticket_router.router)
app.include_router(complex_router.router)