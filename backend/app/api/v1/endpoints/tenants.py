import secrets
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models import Tenant
from app.schemas.all import TenantCreate, TenantRead

router = APIRouter()

@router.post("/", response_model=TenantRead)
async def create_tenant(
    tenant_in: TenantCreate,
    session: AsyncSession = Depends(get_session)
):
    tenant = Tenant.from_orm(tenant_in)
    # Generate unique link token
    tenant.unique_link_token = secrets.token_urlsafe(32)
    
    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)
    return tenant

@router.get("/", response_model=List[TenantRead])
async def read_tenants(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    stmt = select(Tenant).offset(skip).limit(limit)
    result = await session.execute(stmt)
    tenants = result.scalars().all()
    return tenants
