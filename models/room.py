from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.session import Session  

class Room(SQLModel, table=True):
    room_id: Optional[int] = Field(default=None, primary_key=True)
    room_name: str
    capacity: int
    screen_type: str
    audio_system: str
    acessibility: bool

    #Salas 1:N Sessões
    sessions: list["Session"] = Relationship(back_populates="room") 
