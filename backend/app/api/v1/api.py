from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import select, text
from app.api.v1.endpoints import contracts, tenants, payments, whatsapp, properties
from app.db.session import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

api_router = APIRouter()

@api_router.get("/debug-db")
async def debug_db(session: AsyncSession = Depends(get_session)):
    try:
        # List tables
        res_tables = await session.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"))
        tables = res_tables.scalars().all()
        
        counts = {}
        for table in tables:
            try:
                res_count = await session.execute(text(f"SELECT count(*) FROM \"{table}\""))
                counts[table] = res_count.scalar()
            except:
                counts[table] = "error"
                
        return {
            "tables": tables,
            "counts": counts,
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
