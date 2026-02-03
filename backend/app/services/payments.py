from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import Payment, MonthlyCharge, PaymentAllocation, Contract

class PaymentService:
    @staticmethod
    async def process_payment(session: AsyncSession, payment_data: Payment) -> Payment:
        # 1. Save Payment
        session.add(payment_data)
        await session.flush()
        
        # 2. Find pending charges for the tenant
        # We need to find all contracts for this tenant? Or assume payment is linked to a contract?
        # Ideally payment -> Tenant -> Contracts -> Pending Charges
        # Simplified: Get all pending charges for tenant, ordered by due_date
        
        stmt = (
            select(MonthlyCharge)
            .join(Contract)
            .where(Contract.tenant_id == payment_data.tenant_id)
            .where(MonthlyCharge.balance_due > 0)
            .order_by(MonthlyCharge.due_date)
        )
        result = await session.execute(stmt)
        pending_charges = result.scalars().all()
        
        remaining_payment = payment_data.amount
        
        for charge in pending_charges:
            if remaining_payment <= 0:
                break
                
            # Calculate how much to allocate to this charge
            allocation_amount = min(remaining_payment, charge.balance_due)
            
            # Create Allocation
            allocation = PaymentAllocation(
                payment_id=payment_data.id,
                charge_id=charge.id,
                amount_allocated=allocation_amount
            )
            session.add(allocation)
            
            # Update Charge
            charge.balance_due -= allocation_amount
            if charge.balance_due <= 0:
                charge.status = "paid"
            else:
                charge.status = "partial"
            
            session.add(charge)
            
            # Decrement remaining payment
            remaining_payment -= allocation_amount
            
        return payment_data
