import math
from core.logging import logger

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from typing import Optional, List

from models.models import Director
from database.database import get_session
from routers.common import (
    PaginationMeta,
    ListResponseMeta,
    CountResponse,
    DeleteResponse,
    DirectorCreateDTO,
    DirectorUpdateDTO
)

router = APIRouter(prefix="/directors", tags=["Directors"])

@router.post("", response_model=Director)
def create_director(
    directorDto: DirectorCreateDTO,
    session: Session = Depends(get_session)
):
    logger.info(f'[create_director] Creating director {directorDto.director_id}...')
    if directorDto.director_id is not None and session.get(Director, directorDto.director_id):
        logger.error(f'[create_director] A director with id {directorDto.director_id} already exists')
        raise HTTPException(status_code=409, detail="Director with ID already exists")
    director = Director(**directorDto.model_dump(exclude_none=True))
    session.add(director)
    session.commit()
    session.refresh(director)
    logger.info(f'[create_director] Director created successfully!')
    return director

@router.get("", response_model=List[Director])
def list_all_directors(session: Session = Depends(get_session)):
    logger.info(f'[list_all_directors] Listing directors...')
    directors = session.exec(select(Director)).all()
    logger.info(f'[list_all_directors] {len(directors)} found.')
    return directors

@router.get("/filter", response_model=ListResponseMeta[Director])
def filter_directors(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    name_contains: Optional[str] = Query(None, description="Filter by director name"),
    nationaly: Optional[str] = Query(None, description="Filter by nationality")
):
    logger.info(f'[filter_directors] Filtering directors...')
    query = select(Director)

    if name_contains:
        query = query.where(Director.director_name.ilike(f'%{name_contains}%'))

    if nationaly:
        query = query.where(Director.nationality == nationaly)

    total = session.exec(select(func.count()).select_from(query.subquery())).one()
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    offset = (page - 1) * per_page
    directors = session.exec(
        query.offset(offset).limit(per_page)
    ).all()
    remaining = max(total - page * per_page, 0)

    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        remaining=remaining,
    )

    logger.info(f'[filter_directors] {len(directors)} directors found with filters applied.')
    return ListResponseMeta[Director](data=directors, meta=meta)


@router.get("/count", response_model=CountResponse)
def get_director(session: Session = Depends(get_session)):
    logger.info(f'[get_director] Counting directors...')
    total = session.exec(select(func.count()).select_from(Director)).one()
    logger.info(f'[get_director] Total directors: {total}.')
    return CountResponse(quantidade=total)

@router.get("/{director_id}", response_model=Director)
def get_director(
    director_id: int,
    session: Session = Depends(get_session)
):
    logger.info(f'[get_director] Retrieving director with id {director_id}...')
    director = session.get(Director, director_id)
    if not director:
        logger.error(f'[get_director] Director with id {director_id} not found.')
        raise HTTPException(status_code=404, detail="Director not found")
    logger.info(f'[get_director] Director with id {director_id} retrieved successfully.')
    return director

@router.put("/{director_id}", response_model=Director)
def update_director(
    director_id: int,
    directorDto: DirectorUpdateDTO,
    session: Session = Depends(get_session)
):
    logger.info(f'[update_director] Updating director with id {director_id}...')
    existing_director = session.get(Director, director_id)
    if not existing_director:
        logger.error(f'[update_director] Director with id {director_id} not found.')
        raise HTTPException(status_code=404, detail="Director not found")
    
    update_data = directorDto.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_director, key, value)
    
    session.add(existing_director)
    session.commit()
    session.refresh(existing_director)
    logger.info(f'[update_director] Director with id {director_id} updated successfully.')
    return existing_director

@router.delete("/{director_id}", response_model=DeleteResponse)
def delete_director(
    director_id: int,
    session: Session = Depends(get_session)
):
    logger.info(f'[delete_director] Deleting director with id {director_id}...')
    director = session.get(Director, director_id)
    if not director:
        logger.error(f'[delete_director] Director with id {director_id} not found.')
        raise HTTPException(status_code=404, detail="Director not found")
    
    session.delete(director)
    session.commit()
    logger.info(f'[delete_director] Director with id {director_id} deleted successfully.')
    return DeleteResponse(message="Director deleted successfully")