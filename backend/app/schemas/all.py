from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.financial import ContractBase, MonthlyChargeBase
from app.models.payments import PaymentBase
from app.models.base_entities import TenantBase, PropertyBase, AgencyBase

# --- Shared Properties ---
# (Can act as API Request models)

# --- Tenants ---
class TenantCreate(TenantBase):
    agency_id: int

class TenantRead(TenantBase):
    id: int
    agency_id: int
    unique_link_token: str

# --- Properties ---
class PropertyCreate(PropertyBase):
    agency_id: int

class PropertyRead(PropertyBase):
    id: int
    agency_id: int

# --- Contracts ---
class ContractCreate(ContractBase):
    tenant_id: int
    property_id: int

class ContractRead(ContractBase):
    id: int
    tenant_id: int
    property_id: int
    monthly_charges: List["MonthlyChargeRead"] = []

# --- Monthly Charges ---
class MonthlyChargeRead(MonthlyChargeBase):
    id: int
    contract_id: int
    status: str

# --- Payments ---
class PaymentCreate(PaymentBase):
    tenant_id: int

class PaymentRead(PaymentBase):
    id: int
    tenant_id: int
    allocations: List["PaymentAllocationRead"] = []

class PaymentAllocationRead(BaseModel):
    id: int
    charge_id: int
    amount_allocated: float
    charge_month: int
    charge_year: int
