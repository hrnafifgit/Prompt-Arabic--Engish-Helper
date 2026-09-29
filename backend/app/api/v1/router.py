"""API v1 Router Aggregator."""

from fastapi import APIRouter
from backend.app.api.v1.endpoints.prompt import router as prompt_router

api_v1_router = APIRouter()
api_v1_router.include_router(prompt_router)
