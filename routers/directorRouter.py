from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database.database import get_session
from models.models import Director
from pydantic import BaseModel
from typing import List
from sqlalchemy import func
import math

router = APIRouter(prefix="/director", tags=["Directors"])
class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    remaining: int
class DirectorListResponse(BaseModel):
    data: List[Director]
    meta: PaginationMeta

@router.get("", response_model=DirectorListResponse)
def list_directors(
    *,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
):
    total = session.exec(select(func.count()).select_from(Director)).one()
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    offset = (page - 1) * per_page
    directors = session.exec(
        select(Director).offset(offset).limit(per_page)
    ).all()
    remaining = max(total - page * per_page, 0)

    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        remaining=remaining,
    )

    return DirectorListResponse(data=directors, meta=meta)


@router.get("/{director_id}", response_model=Director)
def get_director(
    director_id: int,
    session: Session = Depends(get_session)
):
    director = session.get(Director, director_id)
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director

@router.post("", response_model=Director)
def create_director(
    director: Director,
    session: Session = Depends(get_session)
):
    session.add(director)
    session.commit()
    session.refresh(director)
    return director

@router.put("/{director_id}", response_model=Director)
def update_director(
    director_id: int,
    director: Director,
    session: Session = Depends(get_session)
):
    existing_director = session.get(Director, director_id)
    if not existing_director:
        raise HTTPException(status_code=404, detail="Director not found")
    
    for key, value in director.model_dump(exclude_unset=True).items():
        setattr(existing_director, key, value)
    
    session.add(existing_director)
    session.commit()
    session.refresh(existing_director)
    return existing_director

@router.delete("/{director_id}", response_model=dict)
def delete_director(
    director_id: int,
    session: Session = Depends(get_session)
):
    director = session.get(Director, director_id)
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    
    session.delete(director)
    session.commit()
    return {"message": "Director deleted successfully"}

