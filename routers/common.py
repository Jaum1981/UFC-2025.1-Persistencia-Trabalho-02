import re
from pydantic import BaseModel, field_validator
from typing import Generic, TypeVar, List

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