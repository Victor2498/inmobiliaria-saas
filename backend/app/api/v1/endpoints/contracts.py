from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models import Contract
from app.schemas.all import ContractCreate, ContractRead
from app.services.contracts import ContractService

router = APIRouter()

@router.post("/", response_model=ContractRead)
async def create_contract(
    contract_in: ContractCreate,
    session: AsyncSession = Depends(get_session)
):
    contract = Contract.from_orm(contract_in)
    # Use Service to create charges automatically
    created_contract = await ContractService.create_contract(session, contract)
    await session.commit()
    await session.refresh(created_contract)
    return created_contract

@router.get("/", response_model=List[ContractRead])
async def read_contracts(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    stmt = select(Contract).offset(skip).limit(limit)
    result = await session.execute(stmt)
    contracts = result.scalars().all()
    return contracts

@router.get("/{contract_id}", response_model=ContractRead)
async def read_contract(
    contract_id: int,
    session: AsyncSession = Depends(get_session)
):
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await session.execute(stmt)
    contract = result.scalars().first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract
