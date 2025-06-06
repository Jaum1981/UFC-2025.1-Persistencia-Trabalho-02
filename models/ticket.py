from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from models.payment_details import PaymentDetails

# if TYPE_CHECKING:
#     from models.session import Session

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