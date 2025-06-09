import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from typing import Optional, List

from models.models import Room
from database.database import get_session
from routers.commom import (
    PaginationMeta, 
    ListResponseMeta, 
    CountResponse, 
    DeleteResponse, 
    RoomCreateDTO,
    RoomUpdateDTO
)

router = APIRouter(prefix="/room", tags=["Rooms"])

@router.post("", response_model=Room)
def create_room(
    roomDto: RoomCreateDTO,
    session: Session = Depends(get_session)
):
    if roomDto.room_id is not None:
        existing = session.get(Room, roomDto.room_id)
        if existing:
            raise HTTPException(status_code=409, detail="Room with ID already exists")
    room = Room(**roomDto.model_dump(exclude_none=True))
    session.add(room)
    session.commit()
    session.refresh(room)
    return room

@router.get("", response_model=List[Room])
def list_all_rooms(session: Session = Depends(get_session)):
    rooms = session.exec(select(Room)).all()
    return rooms

@router.get("/filter", response_model=ListResponseMeta[Room])
def filter_rooms(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    room_name_contains: Optional[str] = Query(None, description="Filter by room name"),
    screen_type: Optional[str] = Query(None, description="Filter by screen type"),
    acessibility: Optional[bool] = Query(None, description="Filter by accessibility")
):
    query = select(Room)

    if room_name_contains:
        query = query.where(Room.room_name.ilike(f'%{room_name_contains}%'))

    if screen_type:
        query = query.where(Room.screen_type == screen_type)

    if acessibility is not None:
        query = query.where(Room.acessibility == acessibility)

    total = session.exec(select(func.count()).select_from(query.subquery())).one()
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    offset = (page - 1) * per_page
    rooms = session.exec(query.offset(offset).limit(per_page)).all()

    return ListResponseMeta[Room](
        data=rooms,
        meta=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages,
            remaining=max(0, total - offset - len(rooms))
        )
    )

@router.get("/count", response_model=CountResponse)
def count_rooms(
    session: Session = Depends(get_session)
):
    total = session.exec(select(func.count(Room.room_id))).one()
    return CountResponse(quantidade=total)

@router.get("/{room_id}", response_model=Room)
def get_room(
    room_id: int,
    session: Session = Depends(get_session)
):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.put("/{room_id}", response_model=Room)
def update_room(
    room_id: int,
    roomDto: RoomUpdateDTO,
    session: Session = Depends(get_session)
):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    for key, value in roomDto.model_dump(exclude_none=True).items():
        setattr(room, key, value)

    session.add(room)
    session.commit()
    session.refresh(room)
    return room

@router.delete("/{room_id}", response_model=DeleteResponse)
def delete_room(
    room_id: int,
    session: Session = Depends(get_session)
):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    session.delete(room)
    session.commit()
    return DeleteResponse(message="Room deleted successfully")