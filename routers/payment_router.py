import math
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

from models.models import PaymentDetails
from database.database import get_session
from routers.common import (
    PaginationMeta, 
    ListResponseMeta, 
    CountResponse, 
    DeleteResponse,
    PaymentCreateDTO,
    PaymentUpdateDTO,
)

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("", response_model=PaymentDetails)
def create_payment(
    paymentDto: PaymentCreateDTO,
    session: Session = Depends(get_session)
):
    if paymentDto.payment_id is not None and  session.get(PaymentDetails, paymentDto.payment_id):
        raise HTTPException(status_code=409, detail="Payment with ID already exists")
    data = paymentDto.model_dump(exclude_none=True)
    new_payment = PaymentDetails(**data)
    session.add(new_payment)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="ticket_id does not exist"
        )
    session.refresh(new_payment)
    return new_payment

@router.get("", response_model=List[PaymentDetails])
def list_all_payments(session: Session = Depends(get_session)):
    payments = session.exec(select(PaymentDetails)).all()
    return payments

@router.get("/filter", response_model=ListResponseMeta[PaymentDetails])
def filter_payments(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    transaction_id_contains: Optional[str] = Query(None, description="Filter by transaction ID"),
    payment_method: Optional[str] = Query(None, description="Filter by payment method"),
    status: Optional[str] = Query(None, description="Filter by payment status")
):
    query = select(PaymentDetails)

    if transaction_id_contains:
        query = query.where(PaymentDetails.transaction_id.ilike(f'%{transaction_id_contains}%'))

    if payment_method:
        query = query.where(PaymentDetails.payment_method == payment_method)

    if status:
        query = query.where(PaymentDetails.status == status)

    total = session.exec(select(func.count()).select_from(query.subquery())).one()
    total_pages = math.ceil(total / per_page)
    offset = (page - 1) * per_page

    query = query.offset(offset).limit(per_page)
    payments = session.exec(query).all()

    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        remaining=max(0, total - offset - len(payments))
    )

    return ListResponseMeta[PaymentDetails](data=payments, meta=meta)

@router.get("/count", response_model=CountResponse)
def count_payments(
    session: Session = Depends(get_session)
):
    total = session.exec(select(func.count(PaymentDetails.payment_id))).one()
    return CountResponse(quantidade=total)

@router.get("/{payment_id}", response_model=PaymentDetails)
def get_payment(
    payment_id: int,
    session: Session = Depends(get_session)
):
    payment = session.get(PaymentDetails, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.put("/{payment_id}", response_model=PaymentDetails)
def update_payment(
    payment_id: int,
    paymentDto: PaymentUpdateDTO,
    session: Session = Depends(get_session)
):
    payment = session.get(PaymentDetails, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    update_data = paymentDto.model_dump(exclude_none=True)
    if "payment_date" in update_data:
        update_data["payment_date"] = datetime.strptime(update_data["payment_date"], "%d/%m/%Y %H:%M")
    for key, value in update_data.items():
        setattr(payment, key, value)
    session.add(payment)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="ticket_id does not exist"
        )
    session.refresh(payment)
    return payment

@router.delete("/{payment_id}", response_model=DeleteResponse)
def delete_payment(
    payment_id: int,
    session: Session = Depends(get_session)
):
    payment = session.get(PaymentDetails, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    session.delete(payment)
    session.commit()
    return DeleteResponse(message="Payment deleted successfully")