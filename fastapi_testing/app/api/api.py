from fastapi import APIRouter

from . import health
from .v1.endpoints import login

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
