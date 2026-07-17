from fastapi import APIRouter

from backend.api.v1 import auth
from backend.api.v1.endpoints import telemetry

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    telemetry.router,
    prefix="/telemetry",
    tags=["Telemetry"],
)