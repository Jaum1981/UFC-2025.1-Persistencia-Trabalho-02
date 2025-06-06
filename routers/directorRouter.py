from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.director import Director

router = APIRouter(prefix="/director", tags=["Directors"])

@router.get("", response_model=list[Director])
def list_directors(session: Session = Depends(get_session)):
    return session.exec(select(Director)).all()