from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy import func
from typing import List

from database.database import get_session
from models.models import Movie, Ticket
from models.models import Session as SessionModel
from routers.commom import MovieReport

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/movie-revenue", response_model=List[MovieReport], summary="Gera um relatório de receita por filme")
async def get_movie_revenue_report(session: Session = Depends(get_session)):
    query = (
        select(
            Movie.movie_id,
            Movie.movie_title,
            func.sum(Ticket.ticket_price).label("total_revenue"),
            func.count(Ticket.ticket_id).label("tickets_sold")
        )
        .join(SessionModel, Movie.movie_id == SessionModel.movie_id)
        .join(Ticket, SessionModel.session_id == Ticket.session_id)
        .group_by(Movie.movie_id, Movie.movie_title)
        .order_by(func.sum(Ticket.ticket_price).desc())
    )
    
    results = session.exec(query).all()
    
    report_data = [
        MovieReport(
            movie_id=row.movie_id,
            movie_title=row.movie_title,
            total_revenue=row.total_revenue or 0.0,
            tickets_sold=row.tickets_sold
        ) 
        for row in results
    ]
    
    return report_data