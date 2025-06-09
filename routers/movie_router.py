import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from typing import Optional, List

from models.models import Movie
from database.database import get_session
from routers.commom import (
    PaginationMeta, 
    ListResponseMeta, 
    CountResponse, 
    DeleteResponse, 
    MovieCreateDTO, 
    MovieUpdateDTO
)

router = APIRouter(prefix="/movie", tags=["Movies"])

@router.post("", response_model=Movie)
def create_movie(
    movieDto: MovieCreateDTO,
    session: Session = Depends(get_session)
):
    if movieDto.movie_id is not None:
        existing = session.get(Movie, movieDto.movie_id)
        if existing:
            raise HTTPException(status_code=409, detail="Movie with ID already exists")
    movie = Movie(**movieDto.model_dump(exclude_none=True))
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

@router.get("", response_model=List[Movie])
def list_all_movies(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie)).all()
    return movies

@router.get("/filter", response_model=ListResponseMeta[Movie])
def filter_movies(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    title_contains: Optional[str] = Query(None, description="FilFter by movie title"),
    genre: Optional[str] = Query(None, description="Filter by genre")
):
    query = select(Movie)

    if title_contains:
        query = query.where(Movie.movie_title.ilike(f'%{title_contains}%'))

    if genre:
        query = query.where(Movie.genre == genre)

    total = session.exec(select(func.count()).select_from(query.subquery())).one()
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    offset = (page - 1) * per_page
    movies = session.exec(
        query.offset(offset).limit(per_page)
    ).all()
    remaining = total - (page - 1) * per_page

    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        remaining=remaining,
    )

    return ListResponseMeta(data=movies, meta=meta)

@router.get("/count", response_model=CountResponse)
def count_movies(
    session: Session = Depends(get_session)
):
    total = session.exec(select(func.count(Movie.movie_id))).one()
    return CountResponse(quantidade=total)

@router.get("/{movie_id}", response_model=Movie)
def get_movie(
    movie_id: int,
    session: Session = Depends(get_session)
):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=Movie)
def update_movie(
    movie_id: int,
    movieDto: MovieUpdateDTO,
    session: Session = Depends(get_session)
):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    for key, value in movieDto.model_dump(exclude_none=True).items():
        setattr(movie, key, value)

    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

@router.delete("/{movie_id}", response_model=DeleteResponse)
def delete_movie(
    movie_id: int,
    session: Session = Depends(get_session)
):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    session.delete(movie)
    session.commit()
    return DeleteResponse(message="Movie deleted successfully")
