import re
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
    director_id: int | None = None
    director_name: str
    nationality: str
    birth_date: str
    biography: str
    website: str

    @field_validator('birth_date')
    def validate_birth_date(cls, v):
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', v):
            raise ValueError('birth_date must be DD/MM/YYYY')
        return v
    
    @field_validator('website')
    def validate_website(cls, v):
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('website must start with http:// or https://')
        return v

class DirectorUpdateDTO(BaseModel):
    director_name: str | None = None
    nationality: str | None = None
    birth_date: str | None = None
    biography: str | None = None
    website: str | None = None
    
    @field_validator('birth_date')
    def validate_birth_date(cls, v):
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', v):
            raise ValueError('birth_date must be DD/MM/YYYY')
        return v
    
    @field_validator('website')
    def validate_website(cls, v):
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('website must start with http:// or https://')
        return v
    
class MovieCreateDTO(BaseModel):
    movie_id: int | None = None
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
    room_id: int | None = None
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
    session_id: int | None = None
    date_time: str
    exibition_type: str
    language_audio: str
    language_subtitles: str | None = None
    status_session: str
    room_id: Optional[int]
    movie_id: Optional[int]

    @field_validator('date_time')
    def validate_date_time(cls, v):
        if not re.match(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$', v):
            raise ValueError('date_time must be in DD/MM/YYYY HH:MM format')
        return v
    
class SessionUpdateDTO(BaseModel):
    date_time: str | None = None
    exibition_type: str | None = None
    language_audio: str | None = None
    language_subtitles: str | None = None
    status_session: str | None = None
    room_id: Optional[int] = None
    movie_id: Optional[int] = None

    @field_validator('date_time')
    def validate_date_time(cls, v):
        if v is None:
            return v
        if not re.match(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$', v):
            raise ValueError('date_time must be in DD/MM/YYYY HH:MM format')
        return v
    
class PaymentCreateDTO(BaseModel):
    payment_id: int | None = None
    transaction_id: str
    payment_method: str
    final_price: float
    status: str
    payment_date: str
    ticket_id: Optional[int] = None

    @field_validator('payment_date')
    def validate_payment_date(cls, v):
        if not re.match(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$', v):
            raise ValueError('payment_date must be in DD/MM/YYYY HH:MM format')
        return v
    
class PaymentUpdateDTO(BaseModel):
    transaction_id: str | None = None
    payment_method: str | None = None
    final_price: float | None = None
    status: str | None = None
    payment_date: str | None = None
    ticket_id: Optional[int] = None

    @field_validator('payment_date')
    def validate_payment_date(cls, v):
        if v is not None and not re.match(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$', v):
            raise ValueError('payment_date must be in DD/MM/YYYY HH:MM format')
        return v