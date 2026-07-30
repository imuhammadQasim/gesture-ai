import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import ConnectionFailure

from api.user.router import router as user_router
from core.config import settings
from core.database import Database, mongodb_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events with proper error handling."""
    try:
        logger.info("🚀 Starting up FastAPI application...")
        await Database.connect()
        logger.info("✓ Application startup complete")
    except Exception as e:
        logger.error(f"✗ Startup failed: {e}")
        raise

    yield

    try:
        logger.info("🛑 Shutting down FastAPI application...")
        await Database.disconnect()
        logger.info("✓ Application shutdown complete")
    except Exception as e:
        logger.error(f"✗ Shutdown error: {e}")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint that verifies database connectivity
    
    Returns:
        dict: Health status and database connection status
        
    Raises:
        HTTPException: If database is not connected
    """
    try:
        if mongodb_db is None:
            return {
                "status": "unhealthy",
                "database": "mongodb",
                "message": "Database not connected"
            }

        # Test database connectivity
        await mongodb_db.client.admin.command("ping")

        return {
            "status": "healthy",
            "database": "mongodb",
            "message": "All systems operational"
        }
    except ConnectionFailure as e:
        return {
            "status": "unhealthy",
            "database": "mongodb",
            "message": f"Database connection failed: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "mongodb",
            "message": f"Unexpected error: {str(e)}"
        }
