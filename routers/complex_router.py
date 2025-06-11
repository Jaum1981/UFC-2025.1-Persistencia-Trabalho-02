from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from database.database import get_session
from models.models import Movie, Ticket
from models.models import Session as SessionModel
from routers.common import MovieReport, ListResponseMeta, SessionSummary, PaginationMeta

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/movie-revenue", response_model=List[MovieReport], summary="Gera um relatório de receita por filme")
async def get_movie_revenue_report(order:bool, session: Session = Depends(get_session)):
    
    if order is True:
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
    else:
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
            .order_by(func.sum(Ticket.ticket_price).asc())
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

@router.get("/movie/{movie_id}/sessions", response_model=ListResponseMeta[SessionSummary], summary="Lista sessões de um filme com vendas e receita")
def list_movie_sessions(
    movie_id: int,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    after: Optional[datetime] = Query(None, description="Sessões após esta data/hora"),
    before: Optional[datetime] = Query(None, description="Sessões antes desta data/hora")
):
    query = (
        select(
            SessionModel.session_id,
            SessionModel.date_time,
            SessionModel.exibition_type,
            SessionModel.language_audio,
            SessionModel.language_subtitles,
            SessionModel.status_session,
            func.count(Ticket.ticket_id).label("tickets_sold"),
            func.coalesce(func.sum(Ticket.ticket_price), 0).label("revenue")
        )
        .where(SessionModel.movie_id == movie_id)
        .outerjoin(Ticket, SessionModel.session_id == Ticket.session_id)
        .group_by(
            SessionModel.session_id,
            SessionModel.date_time,
            SessionModel.exibition_type,
            SessionModel.language_audio,
            SessionModel.language_subtitles,
            SessionModel.status_session
        )
        .order_by(SessionModel.date_time)
    )

    if after:
        query = query.where(SessionModel.date_time >= after)
    if before:
        query = query.where(SessionModel.date_time <= before)
    
    total = session.exec(
        select(func.count()).select_from(query.subquery())
    ).one()
    total_pages = (total + per_page - 1)
    offset = (page - 1) * per_page
    results = session.exec(query.offset(offset).limit(per_page)).all()

    items = [SessionSummary(
        session_id=row.session_id,
        date_time=row.date_time,
        exibition_type=row.exibition_type,
        language_audio=row.language_audio,
        language_subtitles=row.language_subtitles,
        status_session=row.status_session,
        tickets_sold=row.tickets_sold,
        revenue=row.revenue
    ) for row in results]

    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        remaining=max(0, total - offset - len(items))
    )

    return ListResponseMeta(data=items, meta=meta)