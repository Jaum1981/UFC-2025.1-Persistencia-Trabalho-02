from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Director(SQLModel, table=True):
    director_id: Optional[int] = Field(default=None, primary_key=True)
    director_name: str
    nationality: str
    birth_date: str
    biography: str
    website: str

    #Filmes n:n Diretores
    movies: List["Movie"] = Relationship(back_populates="directors", link_model="MovieDirectorLink")