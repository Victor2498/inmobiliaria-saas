import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
import sys

# Add backend to path to import models if needed, but we'll use raw SQL
sys.path.append(os.getcwd())

async def check_and_seed():
    from app.core.config import settings
    from app.models.base_entities import Agency
    engine = create_async_engine(str(settings.DATABASE_URI))
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Check version
        try:
            result = await session.execute(text("SELECT version_num FROM alembic_version"))
            version = result.scalar()
            print(f"Alembic Version: {version}")
        except Exception as e:
            print(f"Error checking version: {e}")

        # Check tables
        result = await session.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"))
        tables = result.scalars().all()
        print(f"Existing tables: {tables}")

        if "agency" in tables:
            result = await session.execute(text("SELECT count(*) FROM agency WHERE id = 1"))
            if result.scalar() == 0:
                print("Seeding Agency ID 1...")
                agency = Agency(id=1, name="Inmobiliaria Default")
                session.add(agency)
                await session.commit()
                print("Agency 1 created.")
            else:
                print("Agency 1 already exists.")
        else:
            print("Agency table MISSING!")

if __name__ == "__main__":
    asyncio.run(check_and_seed())
