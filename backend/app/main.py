"""Main FastAPI application entrypoint for PromptCraft AI."""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.core.config import settings
from backend.app.api.v1.router import api_v1_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Smart Arabic-to-English Prompt Engineering & Context Translation Middleware API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 Router
app.include_router(api_v1_router, prefix="/api/v1")

# Mount Frontend directory for direct web access
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")

    @app.get("/", include_in_schema=False)
    async def serve_home():
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/styles.css", include_in_schema=False)
    async def serve_css():
        return FileResponse(FRONTEND_DIR / "styles.css")

    @app.get("/app.js", include_in_schema=False)
    async def serve_js():
        return FileResponse(FRONTEND_DIR / "app.js")
else:
    @app.get("/", tags=["Health Check"])
    async def root():
        return {
            "status": "online",
            "app": settings.APP_NAME,
            "version": "1.0.0",
            "docs": "/docs"
        }


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main.py:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
