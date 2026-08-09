import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.logger import logger
from app.routers import chat, upload, auth
from app.personas.registry import PERSONA_REGISTRY

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Modern lifespan handler — replaces deprecated @app.on_event."""
    # Startup
    from app.models.database import Base, engine
    Base.metadata.create_all(bind=engine)
    logger.info("application_started", version="1.0.0", host=settings.HOST, port=settings.PORT)
    yield
    # Shutdown
    from app.core.cache import cache
    await cache.close()
    logger.info("application_stopped")

app = FastAPI(
    title="Klyvix API",
    version="1.0.0",
    description="Unified API powering 6 specialized AI personas with dual LLM streaming.",
    lifespan=lifespan
)

# CORS setup — allow_credentials=True with ["*"] is invalid per spec,
# so we dynamically set credentials based on whether origins are explicit.
is_wildcard_origins = settings.CORS_ORIGINS == ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=not is_wildcard_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(upload.router)

from fastapi import Response

@app.get("/api/health")
async def health_check(response: Response):
    health_status = {"status": "ok", "service": "Klyvix Backend", "deps": {}}
    
    # 1. Check DB
    from app.models.database import SessionLocal
    from sqlalchemy import text
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health_status["deps"]["database"] = "up"
    except Exception:
        health_status["deps"]["database"] = "down"
        health_status["status"] = "degraded"
        
    # 2. Check Redis
    from app.core.cache import cache
    try:
        await cache.redis.ping()
        health_status["deps"]["redis"] = "up"
    except Exception:
        health_status["deps"]["redis"] = "down"
        health_status["status"] = "degraded"
        
    # 3. Check Qdrant
    from app.core.retrieval import qdrant
    try:
        qdrant.get_collections()
        health_status["deps"]["qdrant"] = "up"
    except Exception:
        health_status["deps"]["qdrant"] = "down"
        health_status["status"] = "degraded"
        
    if health_status["status"] != "ok":
        response.status_code = 503
        
    return health_status

@app.get("/api/personas")
def list_personas():
    """Returns metadata for all available personas."""
    return [
        {
            "id": p.id,
            "display_name": p.display_name,
            "description": p.description,
            "output_mode": p.output_mode,
            "requires_upload": p.requires_upload
        }
        for p in PERSONA_REGISTRY.values()
    ]

# Serve static frontend files if static directory exists
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Klyvix Backend is running. Frontend static files not yet deployed."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
