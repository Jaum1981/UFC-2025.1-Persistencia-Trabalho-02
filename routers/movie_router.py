import math
from core.logging import logger

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from typing import Optional, List

from models.models import Movie
from database.database import get_session
from routers.common import (
    PaginationMeta, 
    ListResponseMeta, 
    CountResponse, 
    DeleteResponse, 
    MovieCreateDTO, 
    MovieUpdateDTO
)

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("", response_model=Movie)
def create_movie(
    movieDto: MovieCreateDTO,
    session: Session = Depends(get_session)
):
    logger.info(f'[create_movie] Creating movie {movieDto.movie_id}...')
    if movieDto.movie_id is not None and session.get(Movie, movieDto.movie_id):
        logger.error(f'[create_movie] A movie with id {movieDto.movie_id} already exists')
        raise HTTPException(status_code=409, detail="Movie with ID already exists")
    movie = Movie(**movieDto.model_dump(exclude_none=True))
    session.add(movie)
    session.commit()
    session.refresh(movie)
    logger.info(f'[create_movie] Movie created successfully!')
    return movie

@router.get("", response_model=List[Movie])
def list_all_movies(session: Session = Depends(get_session)):
    logger.info(f'[list_all_movies] Listing movies...')
    movies = session.exec(select(Movie)).all()
    logger.info(f'[list_all_movies] {len(movies)} found.')
    return movies

@router.get("/filter", response_model=ListResponseMeta[Movie])
def filter_movies(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    title_contains: Optional[str] = Query(None, description="Filter by movie title"),
    genre: Optional[str] = Query(None, description="Filter by genre")
):
    logger.info(f'[filter_movies] Filtering movies...')
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

    logger.info(f'[filter_movies] {len(movies)} movies found with filters applied.')
    return ListResponseMeta[Movie](data=movies, meta=meta)

@router.get("/count", response_model=CountResponse)
def count_movies(
    session: Session = Depends(get_session)
):
    logger.info(f'[count_movies] Counting movies...')
    total = session.exec(select(func.count(Movie.movie_id))).one()
    logger.info(f'[count_movies] Total movies: {total}.')
    return CountResponse(quantidade=total)

@router.get("/{movie_id}", response_model=Movie)
def get_movie_by_id(
    movie_id: int,
    session: Session = Depends(get_session)
):
    logger.info(f'[get_movie_by_id] Retrieving movie with id {movie_id}...')
    movie = session.get(Movie, movie_id)
    if not movie:
        logger.error(f'[get_movie_by_id] Movie with id {movie_id} not found.')
        raise HTTPException(status_code=404, detail="Movie not found")
    logger.info(f'[get_movie_by_id] Movie with id {movie_id} retrieved successfully.')
    return movie

@router.put("/{movie_id}", response_model=Movie)
def update_movie(
    movie_id: int,
    movieDto: MovieUpdateDTO,
    session: Session = Depends(get_session)
):
    logger.info(f'[update_movie] Updating movie with id {movie_id}...')
    movie = session.get(Movie, movie_id)
    if not movie:
        logger.error(f'[update_movie] Movie with id {movie_id} not found.')
        raise HTTPException(status_code=404, detail="Movie not found")
    
    for key, value in movieDto.model_dump(exclude_none=True).items():
        setattr(movie, key, value)

    session.add(movie)
    session.commit()
    session.refresh(movie)
    logger.info(f'[update_movie] Movie with id {movie_id} updated successfully.')
    return movie

@router.delete("/{movie_id}", response_model=DeleteResponse)
def delete_movie(
    movie_id: int,
    session: Session = Depends(get_session)
):
    logger.info(f'[delete_movie] Deleting movie with id {movie_id}...')
    movie = session.get(Movie, movie_id)
    if not movie:
        logger.error(f'[delete_movie] Movie with id {movie_id} not found.')
        raise HTTPException(status_code=404, detail="Movie not found")
    
    session.delete(movie)
    session.commit()
    logger.info(f'[delete_movie] Movie with id {movie_id} deleted successfully.')
    return DeleteResponse(message="Movie deleted successfully")
