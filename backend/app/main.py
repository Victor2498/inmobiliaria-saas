from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
async def seed_data():
    from app.db.session import engine
    from app.models.base_entities import Agency
    from sqlmodel import select
    from sqlmodel.ext.asyncio.session import AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        # Check if any agency exists
        result = await session.execute(select(Agency))
        if not result.first():
            agency = Agency(id=1, name="Inmobiliaria Inmonea")
            session.add(agency)
            await session.commit()
            print("Auto-seeded default agency ID 1")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

from app.api.v1.api import api_router

app.include_router(api_router, prefix=settings.API_V1_STR)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# ... (Existing API routes)

# Mount frontend static files
frontend_dist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")

if os.path.exists(frontend_dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist_path, "assets")), name="assets")

    # SPA Catch-all route
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow API routes to pass through
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return {"status": 404, "message": "Not Found"}
        
        # Serve index.html for everything else
        return FileResponse(os.path.join(frontend_dist_path, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "API running. Frontend not found (dev mode or build missing).", "docs": "/docs"}
