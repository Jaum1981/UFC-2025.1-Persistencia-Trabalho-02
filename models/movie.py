from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class MovieDirectorLink(SQLModel, table=True):
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.movie_id", primary_key=True)
    director_id: Optional[int] = Field(default=None, foreign_key="director.director_id", primary_key=True)

class Movie(SQLModel, table = True):
    movie_id: Optional[int] = Field(default=None, primary_key=True)
    movie_title: str
    genre: str
    duration: int
    rating: str
    synopsis: str

    #Filmes n:n Diretores
    directors: List["Director"] = Relationship(back_populates="movies", link_model=MovieDirectorLink)

    # Filme 1:N Sessões
    sessions: List["Session"] = Relationship(back_populates="movie")