from fastapi import APIRouter
from app.api.v1 import health, gestures, styles, generations, background, users

api_router = APIRouter()

api_router.include_router(health.router, prefix="/api/v1/health", tags=["health"])
api_router.include_router(users.router, prefix="/api/v1/users", tags=["users"])
api_router.include_router(gestures.router, prefix="/api/v1/gestures", tags=["gestures"])
api_router.include_router(styles.router, prefix="/api/v1/styles", tags=["styles"])
api_router.include_router(generations.router, prefix="/api/v1/generations", tags=["generations"])
api_router.include_router(background.router, prefix="/api/v1/background", tags=["background"])
