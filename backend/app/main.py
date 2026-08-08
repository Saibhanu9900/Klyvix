import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.logger import logger
from app.routers import chat, upload, auth
from app.personas.registry import PERSONA_REGISTRY

app = FastAPI(
    title="Klyvix API",
    version="1.0.0",
    description="Unified API powering 6 specialized AI personas with dual LLM streaming."
)

@app.on_event("startup")
async def startup_event():
    logger.info("application_started", version=app.version, host=settings.HOST, port=settings.PORT)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("application_stopped")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(upload.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Klyvix Backend"}

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
