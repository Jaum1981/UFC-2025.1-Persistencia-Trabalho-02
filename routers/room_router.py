import math
from core.logging import logger

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from typing import Optional, List

from models.models import Room
from database.database import get_session
from routers.common import (
    PaginationMeta, 
    ListResponseMeta, 
    CountResponse, 
    DeleteResponse, 
    RoomCreateDTO,
    RoomUpdateDTO
)

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("", response_model=Room)
def create_room(
    roomDto: RoomCreateDTO,
    session: Session = Depends(get_session)
):
    logger.info(f'[create_room] Creating room {roomDto.room_id}...')
    if roomDto.room_id is not None:
        existing = session.get(Room, roomDto.room_id)
        if existing:
            logger.error(f'[create_room] A room with id {roomDto.room_id} already exists')
            raise HTTPException(status_code=409, detail="Room with ID already exists")
    room = Room(**roomDto.model_dump(exclude_none=True))
    session.add(room)
    session.commit()
    session.refresh(room)
    logger.info(f'[create_room] Room created successfully!')
    return room

@router.get("", response_model=List[Room])
def list_all_rooms(session: Session = Depends(get_session)):
    logger.info(f'[list_all_rooms] Listing all rooms...')
    rooms = session.exec(select(Room)).all()
    logger.info(f'[list_all_rooms] {len(rooms)} rooms found.')
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
    logger.info(f'[filter_rooms] Filtering rooms...')
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

    logger.info(f'[filter_rooms] {len(rooms)} rooms found with filters applied.')
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
    logger.info(f'[count_rooms] Counting rooms...')
    total = session.exec(select(func.count(Room.room_id))).one()
    logger.info(f'[count_rooms] Total rooms: {total}.')
    return CountResponse(quantidade=total)

@router.get("/{room_id}", response_model=Room)
def get_room(
    room_id: int,
    session: Session = Depends(get_session)
):
    logger.info(f'[get_room] Retrieving room with id {room_id}...')
    room = session.get(Room, room_id)
    if not room:
        logger.error(f'[get_room] Room with id {room_id} not found.')
        raise HTTPException(status_code=404, detail="Room not found")
    logger.info(f'[get_room] Room with id {room_id} retrieved successfully.')
    return room

@router.put("/{room_id}", response_model=Room)
def update_room(
    room_id: int,
    roomDto: RoomUpdateDTO,
    session: Session = Depends(get_session)
):
    logger.info(f'[update_room] Updating room with id {room_id}...')
    room = session.get(Room, room_id)
    if not room:
        logger.error(f'[update_room] Room with id {room_id} not found.')
        raise HTTPException(status_code=404, detail="Room not found")
    
    for key, value in roomDto.model_dump(exclude_none=True).items():
        setattr(room, key, value)

    session.add(room)
    session.commit()
    session.refresh(room)
    logger.info(f'[update_room] Room with id {room_id} updated successfully.')
    return room

@router.delete("/{room_id}", response_model=DeleteResponse)
def delete_room(
    room_id: int,
    session: Session = Depends(get_session)
):
    logger.info(f'[delete_room] Deleting room with id {room_id}...')
    room = session.get(Room, room_id)
    if not room:
        logger.error(f'[delete_room] Room with id {room_id} not found.')
        raise HTTPException(status_code=404, detail="Room not found")
    
    session.delete(room)
    session.commit()
    logger.info(f'[delete_room] Room with id {room_id} deleted successfully.')
    return DeleteResponse(message="Room deleted successfully")