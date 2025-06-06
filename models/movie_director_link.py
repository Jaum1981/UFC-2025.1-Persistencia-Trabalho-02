from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional

class MovieDirectorLink(SQLModel, table=True):
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.movie_id", primary_key=True)
    director_id: Optional[int] = Field(default=None, foreign_key="director.director_id", primary_key=True)
