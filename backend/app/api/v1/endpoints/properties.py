from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.session import get_session
from app.models.base_entities import Property
from app.schemas.all import PropertyCreate, PropertyRead
from typing import List

router = APIRouter()

@router.get("/", response_model=List[PropertyRead])
async def list_properties(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Property))
    return result.scalars().all()

@router.post("/", response_model=PropertyRead)
async def create_property(prop_in: PropertyCreate, session: AsyncSession = Depends(get_session)):
    prop = Property.from_orm(prop_in)
    session.add(prop)
    await session.commit()
    await session.refresh(prop)
    return prop
