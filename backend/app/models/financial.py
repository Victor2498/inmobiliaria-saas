from datetime import date, datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .base_entities import TimeStampedModel

class ContractBase(SQLModel):
    start_date: date
    end_date: date
    initial_amount: float
    current_amount: float
    billing_day: int = 1 # Day of month to generate billing
    status: str = "active" # active, completed, terminated
    
class Contract(ContractBase, TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    tenant_id: int = Field(foreign_key="tenant.id")
    tenant: "Tenant" = Relationship(back_populates="contracts")
    
    property_id: int = Field(foreign_key="property.id")
    property: "Property" = Relationship(back_populates="contracts")
    
    monthly_charges: List["MonthlyCharge"] = Relationship(back_populates="contract")

class MonthlyChargeBase(SQLModel):
    month: int
    year: int
    due_date: date
    # Breakdown of amounts
    rent_amount: float
    expenses_amount: float = 0
    water_amount: float = 0
    other_amount: float = 0
    surcharge_amount: float = 0 # Punitorios
    discount_amount: float = 0
    
    total_amount: float # Calculated sum
    balance_due: float # Pending amount (starts as total_amount)
    
    status: str = "pending" # pending, partial, paid, overdue
    is_generated: bool = True # Flag to show it was auto-generated
    
class MonthlyCharge(MonthlyChargeBase, TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    contract_id: int = Field(foreign_key="contract.id")
    contract: Optional[Contract] = Relationship(back_populates="monthly_charges")
    
    payment_allocations: List["PaymentAllocation"] = Relationship(back_populates="charge")
