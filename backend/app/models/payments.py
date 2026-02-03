from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .base_entities import TimeStampedModel

class PaymentBase(SQLModel):
    amount: float
    payment_date: datetime
    method: str # cash, transfer, etc.
    reference: Optional[str] = None # Comprobante
    notes: Optional[str] = None

class Payment(PaymentBase, TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Can initiate a payment without a contract? Ideally no, but maybe "Unidentified"
    # For now, linking to a Tenant is enough, or directly to allocations.
    # Actually, usually payments are from a Tenant.
    tenant_id: Optional[int] = Field(default=None, foreign_key="tenant.id")
    
    allocations: List["PaymentAllocation"] = Relationship(back_populates="payment")

class PaymentAllocation(SQLModel, table=True):
    """
    Join table to link a single Payment to one or multiple MonthlyCharges.
    Example: Payment of $200 allocated to: 
    - Charge Jan ($100)
    - Charge Feb ($100)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    payment_id: int = Field(foreign_key="payment.id")
    payment: Optional[Payment] = Relationship(back_populates="allocations")
    
    charge_id: int = Field(foreign_key="monthlycharge.id")
    charge: "MonthlyCharge" = Relationship(back_populates="payment_allocations")
    
    amount_allocated: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
