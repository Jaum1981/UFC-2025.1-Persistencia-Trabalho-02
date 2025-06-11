import re
from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T') # Tipo genérico

class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    remaining: int

class ListResponseMeta(BaseModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta

class CountResponse(BaseModel):
    quantidade: int

class DeleteResponse(BaseModel):
    message: str

class DirectorCreateDTO(BaseModel):
    director_id: Optional[int]
    director_name: str
    nationality: str
    birth_date: datetime
    biography: str
    website: str

    @field_validator('website')
    def validate_website(cls, v):
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('website must start with http:// or https://')
        return v

class DirectorUpdateDTO(BaseModel):
    director_name: str | None = None
    nationality: str | None = None
    birth_date: datetime | None = None
    biography: str | None = None
    website: str | None = None
    
    @field_validator('website')
    def validate_website(cls, v):
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('website must start with http:// or https://')
        return v
    
class MovieCreateDTO(BaseModel):
    movie_id: Optional[int]
    movie_title: str
    genre: str
    duration: int
    rating: str
    synopsis: str
    
class MovieUpdateDTO(BaseModel):
    movie_title: str | None = None
    genre: str | None = None
    duration: int | None = None
    rating: str | None = None
    synopsis: str | None = None

class RoomCreateDTO(BaseModel):
    room_id: Optional[int]
    room_name: str
    capacity: int
    screen_type: str
    audio_system: str
    acessibility: bool

class RoomUpdateDTO(BaseModel):
    room_name: str | None = None
    capacity: int | None = None
    screen_type: str | None = None
    audio_system: str | None = None
    acessibility: bool | None = None

class SessionCreateDTO(BaseModel):
    session_id: Optional[int]
    date_time: datetime
    exibition_type: str
    language_audio: str
    language_subtitles: str | None = None
    status_session: str
    room_id: Optional[int]
    movie_id: Optional[int]
    
class SessionUpdateDTO(BaseModel):
    date_time: datetime | None = None
    exibition_type: str | None = None
    language_audio: str | None = None
    language_subtitles: str | None = None
    status_session: str | None = None
    room_id: Optional[int] = None
    movie_id: Optional[int] = None
    
class PaymentCreateDTO(BaseModel):
    payment_id: Optional[int]
    transaction_id: str
    payment_method: str
    final_price: float
    status: str
    payment_date: datetime
    ticket_id: Optional[int] = None
    
class PaymentUpdateDTO(BaseModel):
    transaction_id: str | None = None
    payment_method: str | None = None
    final_price: float | None = None
    status: str | None = None
    payment_date: datetime | None = None
    ticket_id: Optional[int] = None
    
class TicketCreateDTO(BaseModel):
    ticket_id: Optional[int]
    chair_number: int
    ticket_type: str
    ticket_price: float
    purchase_date: datetime
    payment_status: str
    session_id: Optional[int] = None
    
class TicketUpdateDTO(BaseModel):
    chair_number: int | None = None
    ticket_type: str | None = None
    ticket_price: float | None = None
    purchase_date: datetime | None = None
    payment_status: str | None = None
    session_id: Optional[int] = None

class SessionSummary(BaseModel):
    session_id: int
    date_time: datetime
    exibition_type: str
    language_audio: str
    language_subtitles: Optional[str]
    status_session: str
    tickets_sold: int
    revenue: float

class MovieReport(BaseModel):
    movie_id: int
    movie_title: str
    total_revenue: float
    tickets_sold: int
