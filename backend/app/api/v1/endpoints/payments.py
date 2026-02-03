from typing import List
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models import Payment
from app.schemas.all import PaymentCreate, PaymentRead
from app.services.payments import PaymentService

router = APIRouter()

@router.post("/", response_model=PaymentRead)
async def create_payment(
    payment_in: PaymentCreate,
    session: AsyncSession = Depends(get_session)
):
    payment = Payment.from_orm(payment_in)
    # Use Service to allocate payment automatically
    created_payment = await PaymentService.process_payment(session, payment)
    await session.commit()
    await session.refresh(created_payment)
    return created_payment

@router.get("/", response_model=List[PaymentRead])
async def read_payments(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    stmt = select(Payment).offset(skip).limit(limit)
    result = await session.execute(stmt)
    payments = result.scalars().all()
    return payments
