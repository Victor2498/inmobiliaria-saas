import sys
import os
import asyncio
from datetime import date, datetime, timedelta

# Add backend to sys.path to ensure imports work from root
backend_path = os.path.join(os.getcwd(), 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.models import Agency, User, Property, Tenant, Contract, Payment
from app.services.contracts import ContractService
from app.services.payments import PaymentService

async def seed():
    print("Seeding data...")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 1. Create Agency
        agency = Agency(
            name="Inmobiliaria Modelo", 
            phone="11-1234-5678", 
            email="info@modelo.com"
        )
        session.add(agency)
        await session.commit()
        await session.refresh(agency)
        print(f"✅ Agency created: {agency.name}")

        # 2. Create Properties
        props = [
            Property(address="Av. Libertador 2400, 5A", city="CABA", type="apartment", status="rented", price=450000, agency_id=agency.id),
            Property(address="Charcas 3500, PB", city="CABA", type="apartment", status="available", price=320000, agency_id=agency.id),
            Property(address="Gorriti 5500", city="CABA", type="local", status="rented", price=850000, agency_id=agency.id)
        ]
        for p in props:
            session.add(p)
        await session.commit()
        for p in props: await session.refresh(p)
        print(f"✅ {len(props)} Properties created.")

        # 3. Create Tenant
        tenant = Tenant(
            full_name="Martín Inquilino", 
            phone="5491199998888", 
            email="martin@email.com", 
            unique_link_token="token_seguro_martin",
            agency_id=agency.id
        )
        session.add(tenant)
        await session.commit()
        await session.refresh(tenant)
        print(f"✅ Tenant created: {tenant.full_name}")

        # 4. Create Contract (Libertador)
        # Starts 2 months ago to have some history
        start_date = date.today() - timedelta(days=60)
        contract = Contract(
            start_date=start_date,
            end_date=start_date + timedelta(days=365*2), # 2 years
            initial_amount=450000,
            current_amount=450000,
            billing_day=5,
            tenant_id=tenant.id,
            property_id=props[0].id # Libertador
        )
        # Use Service to generate charges
        await ContractService.create_contract(session, contract)
        await session.commit()
        print("✅ Contract created for Libertador (with monthly charges).")

        # 5. Create Another Contract (Gorriti)
        contract2 = Contract(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365*3),
            initial_amount=850000,
            current_amount=850000,
            billing_day=10,
            tenant_id=tenant.id, # Same tenant for demo
            property_id=props[2].id # Gorriti
        )
        await ContractService.create_contract(session, contract2)
        await session.commit()
        print("✅ Contract created for Gorriti.")

        # 6. Pay the first month of Libertador partially
        # Total due is likely huge if we consider all generated months? 
        # Actually logic generated future months too. Payment Service checks due_date order?
        # Let's pay 500,000. Should cover 1st month (450k) + 50k of 2nd month.
        payment = Payment(
            amount=500000, 
            payment_date=datetime.now(), 
            method="transfer", 
            tenant_id=tenant.id,
            notes="Pago inicial demo"
        )
        await PaymentService.process_payment(session, payment)
        await session.commit()
        print("✅ Payment of $500,000 processed.")

    print("\n🎉 Seed completed successfully!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
