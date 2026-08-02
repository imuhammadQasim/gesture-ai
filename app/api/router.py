from fastapi import APIRouter
from app.api.v1 import health, gestures, styles, generations, background, users

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(gestures.router, prefix="/gestures", tags=["gestures"])
api_router.include_router(styles.router, prefix="/styles", tags=["styles"])
api_router.include_router(generations.router, prefix="/generations", tags=["generations"])
api_router.include_router(background.router, prefix="/background", tags=["background"])
