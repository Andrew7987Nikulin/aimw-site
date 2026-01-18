from fastapi import APIRouter
from .v1.health import router as health_router
from .v1.chat import router as chat_router
from .v1.memory import router as memory_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(chat_router, tags=["chat"])
api_router.include_router(memory_router, tags=["memory"])
