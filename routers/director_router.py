import math

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
    if directorDto.director_id is not None:
        existing = session.get(Director, directorDto.director_id)
        if existing:
            raise HTTPException(status_code=409, detail="Director with ID alredy exists")
    director = Director(**directorDto.model_dump(exclude_none=True))
    session.add(director)
    session.commit()
    session.refresh(director)
    return director

@router.get("", response_model=List[Director])
def list_all_directors(session: Session = Depends(get_session)):
    directors = session.exec(select(Director)).all()
    return directors

@router.get("/filter", response_model=ListResponseMeta[Director])
def filter_directors(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    name_contains: Optional[str] = Query(None, description="Filter by direction name"),
    nationaly: Optional[str] = Query(None, description="Filter by nationality")
):
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

    return ListResponseMeta[Director](data=directors, meta=meta)


@router.get("/count", response_model=CountResponse)
def get_director(session: Session = Depends(get_session)):
    total = session.exec(select(func.count()).select_from(Director)).one()
    return CountResponse(quantidade=total)

@router.get("/{director_id}", response_model=Director)
def get_director(
    director_id: int,
    session: Session = Depends(get_session)
):
    director = session.get(Director, director_id)
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director

@router.put("/{director_id}", response_model=Director)
def update_director(
    director_id: int,
    directorDto: DirectorUpdateDTO,
    session: Session = Depends(get_session)
):
    existing_director = session.get(Director, director_id)
    if not existing_director:
        raise HTTPException(status_code=404, detail="Director not found")
    
    update_data = directorDto.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_director, key, value)
    
    session.add(existing_director)
    session.commit()
    session.refresh(existing_director)
    return existing_director

@router.delete("/{director_id}", response_model=DeleteResponse)
def delete_director(
    director_id: int,
    session: Session = Depends(get_session)
):
    director = session.get(Director, director_id)
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    
    session.delete(director)
    session.commit()
    return DeleteResponse(message="Director deleted successfully")