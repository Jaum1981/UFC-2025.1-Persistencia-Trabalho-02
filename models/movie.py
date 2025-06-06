from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from models.movie_director_link import MovieDirectorLink  

if TYPE_CHECKING:
    from models.director import Director
    from models.session import Session  

class Movie(SQLModel, table = True):
    movie_id: Optional[int] = Field(default=None, primary_key=True)
    movie_title: str
    genre: str
    duration: int
    rating: str
    synopsis: str

    #Filmes n:n Diretores
    directors: list["Director"] = Relationship(back_populates="movies", link_model=MovieDirectorLink)

    # Filme 1:N Sessões
    sessions: list["Session"] = Relationship(back_populates="movie")