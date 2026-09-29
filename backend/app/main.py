"""Main FastAPI application entrypoint for PromptCraft AI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "optimize": "/api/v1/prompt/optimize",
            "execute": "/api/v1/prompt/execute",
            "domains": "/api/v1/prompt/domains",
            "templates": "/api/v1/prompt/templates"
        }
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main.py:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
