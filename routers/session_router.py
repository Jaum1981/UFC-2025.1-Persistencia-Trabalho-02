import math
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

from core.logging import logger
from models.models import Session as SessionModel
from models.models import Movie, Room
from database.database import get_session
from routers.common import (
    PaginationMeta, 
    ListResponseMeta, 
    CountResponse, 
    DeleteResponse, 
    SessionCreateDTO,
    SessionUpdateDTO
)

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("", response_model=SessionModel)
def create_session(
    sessionDto: SessionCreateDTO,
    session: Session = Depends(get_session)
):
    logger.info(f'[create_session] Creating session {sessionDto.session_id}...')
    if sessionDto.session_id is not None and session.get(SessionModel, sessionDto.session_id):
        logger.error(f'[create_session] A session with id {sessionDto.session_id} already exists')
        raise HTTPException(status_code=409, detail="Session with ID already exists")
    data = sessionDto.model_dump(exclude_none=True)
    new_session = SessionModel(**data)
    session.add(new_session)
    try:
        session.commit()
        session.refresh(new_session)
        logger.info(f'[create_session] Session created successfully!')
    except IntegrityError:
        session.rollback()
        logger.error(f'[create_session] Integrity error: room_id or movie_id do not exist')
        raise HTTPException(
            status_code=400,
            detail="room_id ou movie_id não existem"
        )
    return new_session

@router.get("", response_model=List[SessionModel])
def list_all_sessions(session: Session = Depends(get_session)):
    logger.info(f'[list_all_sessions] Listing all sessions...')
    sessions = session.exec(select(SessionModel)).all()
    logger.info(f'[list_all_sessions] {len(sessions)} sessions found.')
    return sessions

@router.get("/filter", response_model=ListResponseMeta[SessionModel])
def filter_sessions(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    after: Optional[datetime] = Query(None, description="Sessions from"),
    before: Optional[datetime] = Query(None, description="Sessions until"),
    status_session: Optional[str] = Query(None, description="Filter by session status"),
    room_id: Optional[int] = Query(None, description="Filter by room ID"),
    movie_id: Optional[int] = Query(None, description="Filter by movie ID")
):
    logger.info(f'[filter_sessions] Filtering sessions...')
    query = select(SessionModel)

    if after:
        query = query.where(SessionModel.date_time >= after)
    if before:
        query = query.where(SessionModel.date_time <= before)

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

    logger.info(f'[filter_sessions] {len(sessions)} sessions found with filters applied.')
    return ListResponseMeta[SessionModel](
        data=sessions, meta=meta)

@router.get("/count", response_model=CountResponse)
def count_sessions(
    session: Session = Depends(get_session)
):
    logger.info(f'[count_sessions] Counting sessions...')
    total = session.exec(select(func.count(SessionModel.session_id))).one()
    logger.info(f'[count_sessions] Total sessions: {total}.')
    return CountResponse(quantidade=total)

@router.get("/{session_id}", response_model=SessionModel)
def get_session_by_id(
    session_id: int,
    session_session: Session = Depends(get_session)
):
    logger.info(f'[get_session_by_id] Retrieving session with id {session_id}...')
    session_data = session_session.get(SessionModel, session_id)
    if not session_data:
        logger.error(f'[get_session_by_id] Session with id {session_id} not found.')
        raise HTTPException(status_code=404, detail="Session not found")
    logger.info(f'[get_session_by_id] Session with id {session_id} retrieved successfully.')
    return session_data

@router.put("/{session_id}", response_model=SessionModel)
def update_session(
    session_id: int,
    sessionDto: SessionUpdateDTO,
    session: Session = Depends(get_session)
):
    logger.info(f'[update_session] Updating session with id {session_id}...')
    existing_session = session.get(SessionModel, session_id)
    if not existing_session:
        logger.error(f'[update_session] Session with id {session_id} not found.')
        raise HTTPException(status_code=404, detail="Session not found")
    
    update_data = sessionDto.model_dump(exclude_none=True)
    if "date_time" in update_data and update_data["date_time"] is not None:
        update_data["date_time"] = datetime.strptime(update_data["date_time"], "%d/%m/%Y %H:%M")

    for key, value in update_data.items():
        setattr(existing_session, key, value)

    session.add(existing_session)
    try:
        session.commit()
        logger.info(f'[update_session] Session with id {session_id} updated successfully.')
    except IntegrityError:
        session.rollback()
        logger.error(f'[update_session] Integrity error: room_id or movie_id do not exist')
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
    logger.info(f'[delete_session] Deleting session with id {session_id}...')
    existing_session = session.get(SessionModel, session_id)
    if not existing_session:
        logger.error(f'[delete_session] Session with id {session_id} not found.')
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.delete(existing_session)
    session.commit()
    logger.info(f'[delete_session] Session with id {session_id} deleted successfully.')
    return DeleteResponse(message="Session deleted successfully")