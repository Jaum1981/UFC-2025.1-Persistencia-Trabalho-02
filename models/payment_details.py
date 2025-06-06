from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

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