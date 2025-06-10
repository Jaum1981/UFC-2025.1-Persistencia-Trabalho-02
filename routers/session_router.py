import math
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

from models.models import Session as SessionModel
from models.models import Movie, Room
from database.database import get_session
from routers.commom import (
    PaginationMeta, 
    ListResponseMeta, 
    CountResponse, 
    DeleteResponse, 
    SessionCreateDTO,
    SessionUpdateDTO
)

router = APIRouter(prefix="/session", tags=["Sessions"])

@router.post("", response_model=SessionModel)
def create_session(
    sessionDto: SessionCreateDTO,
    session: Session = Depends(get_session)
):
    if sessionDto.session_id is not None:
        existing = session.get(SessionModel, sessionDto.session_id)
        if existing:
            raise HTTPException(status_code=409, detail="Session with ID already exists")
    data = sessionDto.model_dump(exclude_none=True)
    data["date_time"] = datetime.strptime(data["date_time"], "%d/%m/%Y %H:%M")
    new_session = SessionModel(**data)
    session.add(new_session)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="room_id ou movie_id não existem"
        )
    session.commit()
    session.refresh(new_session)
    return new_session

@router.get("", response_model=List[SessionModel])
def list_all_sessions(session: Session = Depends(get_session)):
    sessions = session.exec(select(SessionModel)).all()
    return sessions

@router.get("/filter", response_model=ListResponseMeta[SessionModel])
def filter_sessions(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    date_time: Optional[str] = Query(None, description="Filter by session date and time"),
    status_session: Optional[str] = Query(None, description="Filter by session status"),
    room_id: Optional[int] = Query(None, description="Filter by room ID"),
    movie_id: Optional[int] = Query(None, description="Filter by movie ID")
):
    query = select(SessionModel)

    if date_time:
        query = query.where(SessionModel.date_time.ilike(f'%{date_time}%'))

    if status_session:
        query = query.where(SessionModel.status_session == status_session)

    if room_id is not None:
        query = query.where(SessionModel.room_id == room_id)

    if movie_id is not None:
        query = query.where(SessionModel.movie_id == movie_id)

    total = session.exec(select(func.count()).select_from(query.subquery())).one()
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    offset = (page - 1) * per_page
    sessions = session.exec(query.offset(offset).limit(per_page)).all()
    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        remaining= max(0, total - offset - len(sessions))
    )

    return ListResponseMeta[SessionModel](
        data=sessions, meta=meta)

@router.get("/count", response_model=CountResponse)
def count_sessions(
    session: Session = Depends(get_session)
):
    total = session.exec(select(func.count(SessionModel.session_id))).one()
    return CountResponse(quantidade=total)

@router.get("/{session_id}", response_model=SessionModel)
def get_session_by_id(
    session_id: int,
    session_session: Session = Depends(get_session)
):
    session_data = session_session.get(SessionModel, session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_data

@router.put("/{session_id}", response_model=SessionModel)
def update_session(
    session_id: int,
    sessionDto: SessionUpdateDTO,
    session: Session = Depends(get_session)
):
    existing_session = session.get(SessionModel, session_id)
    if not existing_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    update_data = sessionDto.model_dump(exclude_none=True)
    if "date_time" in update_data and update_data["date_time"] is not None:
        update_data["date_time"] = datetime.strptime(update_data["date_time"], "%d/%m/%Y %H:%M")

    for key, value in update_data.items():
        setattr(existing_session, key, value)

    session.add(existing_session)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="room_id ou movie_id não existem"
        )
    session.refresh(existing_session)
    return existing_session

@router.delete("/{session_id}", response_model=DeleteResponse)
def delete_session(
    session_id: int,
    session: Session = Depends(get_session)
):
    existing_session = session.get(SessionModel, session_id)
    if not existing_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.delete(existing_session)
    session.commit()
    return DeleteResponse(message="Session deleted successfully")