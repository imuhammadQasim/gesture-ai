import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.db import create_db_and_tables
from app.core.cloudinary import init_cloudinary

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting up FastAPI application...")
        create_db_and_tables()
        init_cloudinary()
        yield
    except Exception as e:
        logger.error(f"Error starting up FastAPI application: {e}")
        raise
    finally:
        logger.info("Shutting down FastAPI application...")

app = FastAPI(
    title="Gesture AI",
    description="Backend API for the Gesture AI SaaS Platform",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
