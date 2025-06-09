from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

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
    directors: list["Director"] = Relationship(back_populates="movies", link_model=MovieDirectorLink)

    # Filme 1:N Sessões
    sessions: list["Session"] = Relationship(back_populates="movie")

class Director(SQLModel, table=True):
    director_id: Optional[int] = Field(default=None, primary_key=True)
    director_name: str
    nationality: str
    birth_date: str
    biography: str
    website: str

    #Filmes n:n Diretores
    movies: list["Movie"] = Relationship(back_populates="directors", link_model=MovieDirectorLink) 


class PaymentDetails(SQLModel, table=True):
    payment_id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: str
    payment_method: str
    final_price: float
    status: str
    payment_date: datetime

    # Tickets 1:1 PaymentDetails
    ticket_id: Optional[int] = Field(default=None, foreign_key="ticket.ticket_id")
    ticket: Optional["Ticket"] = Relationship(back_populates="payment_details")

class Room(SQLModel, table=True):
    room_id: Optional[int] = Field(default=None, primary_key=True)
    room_name: str
    capacity: int
    screen_type: str
    audio_system: str
    acessibility: bool

    #Salas 1:N Sessões
    sessions: list["Session"] = Relationship(back_populates="room") 

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

class Ticket(SQLModel, table=True):
    ticket_id: Optional[int] = Field(default=None, primary_key=True)
    chair_number: int
    ticket_type: str
    ticket_price: float
    purchase_date: datetime
    payment_status: str

    # tickets 1:1 PaymentDetails
    payment_details: Optional["PaymentDetails"] = Relationship(back_populates="ticket") 

    # ticket 1:N sessao
    session_id: Optional[int] = Field(default=None, foreign_key="session.session_id")
    session: Optional["Session"] = Relationship(back_populates="tickets")  