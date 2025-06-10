import math
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

from models.models import Ticket
from database.database import get_session
from routers.commom import (
    PaginationMeta, 
    ListResponseMeta, 
    CountResponse, 
    DeleteResponse,
    TickerCreateDTO,
    TicketUpdateDTO
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("", response_model=Ticket)
def create_ticket(
    ticketDto: TickerCreateDTO,
    session: Session = Depends(get_session)
):
    if ticketDto.ticket_id is not None:
        existing = session.get(Ticket, ticketDto.ticket_id)
        if existing:
            raise HTTPException(status_code=409, detail="Ticket with ID already exists")
    data = ticketDto.model_dump(exclude_none=True)
    if "purchase_date" in data:
        data["purchase_date"] = datetime.strptime(data["purchase_date"], "%d/%m/%Y %H:%M")
        new_ticket = Ticket(**data)
        session.add(new_ticket)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400,
                detail="session_id does not exist"
                )
        session.commit()
        session.refresh(new_ticket)
        return new_ticket
    
@router.get("", response_model=List[Ticket])
def list_all_tickets(session: Session = Depends(get_session)):
    tickets = session.exec(select(Ticket)).all()
    return tickets


@router.get("/filter", response_model=ListResponseMeta[Ticket])
def filter_tickets(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    chair_number: Optional[str] = Query(None, description="Filter by chair number"),
    ticket_type: Optional[str] = Query(None, description="Filter by ticket type"),
    purchase_date: Optional[str] = Query(None, description="Filter by purchase date"),
    payment_status: Optional[str] = Query(None, description="Filter by payment status")
):
    query = select(Ticket)

    if chair_number:
        query = query.where(Ticket.chair_number == chair_number)
    
    if ticket_type:
        query = query.where(Ticket.ticket_type == ticket_type)

    if purchase_date:
        query = query.where(Ticket.purchase_date == purchase_date)

    if payment_status:
        query = query.where(Ticket.payment_status == payment_status)
    
    total = session.exec(select(func.count()).select_from(query.subquery())).one()
    total_pages = math.ceil(total / per_page)
    offset = (page - 1) * per_page

    query = query.offset(offset).limit(per_page)
    tickets = session.exec(query).all()

    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        remaining=max(0, total - offset - len(tickets))
    )

    return ListResponseMeta[Ticket](data=tickets, meta=meta)
    

@router.get("/count", response_model=CountResponse)
def count_tickets(
    session: Session = Depends(get_session)
):
    total = session.exec(select(func.count(Ticket.ticket_id))).one
    return CountResponse(quantidade=total)

@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket_by_id(
    ticket_id: int,
    session: Session = Depends(get_session)
):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("{ticket_id}", response_model=Ticket)
def update_ticket(
    ticket_id: int,
    tickeDto: TicketUpdateDTO,
    session: Session = Depends(get_session)
):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    update_data = tickeDto.model_dump(exclude_none=True)
    if "purchase_date" in update_data:
        update_data["purchase_date"] = datetime.strftime(update_data["purchase_date"], "%d/%m/%Y %H:%M")
    for key, value in update_data.items():
        setattr(ticket, key, value)
    session.add(ticket)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Session_id does not exist"
        )
    session.refresh(ticket)
    return ticket

@router.delete("/{ticket_id}", response_model=DeleteResponse)
def delete_ticket(
    ticket_id: int,
    session: Session = Depends(get_session)
):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    session.delete(ticket)
    session.commit()
    return DeleteResponse(message="Ticket deleted successfully")