from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.room import Room  
    from models.movie import Movie  
    from models.ticket import Ticket  

class Session(SQLModel, table=True):
    session_id: Optional[int] = Field(default=None, primary_key=True)
    date_time: datetime
    exibition_type: str
    language_audio: str
    language_subtitles: str
    status_session: str

    #Salas 1:N Sessões
    room_id: Optional[int] = Field(default=None, foreign_key="room.room_id")
    room: Optional["Room"] = Relationship(back_populates="sessions") 

    #Movie 1:N Sessões
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.movie_id")
    movie: Optional["Movie"] = Relationship(back_populates="sessions")

    # Sessão 1:N Tickets
    tickets: list["Ticket"] = Relationship(back_populates="session") 