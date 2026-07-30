"""
MongoDB Connection Module with Connection Pooling and Retry Logic
"""

import asyncio
import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# ==================== MongoDB Setup ====================
mongodb_client: Optional[AsyncIOMotorClient] = None
mongodb_db: Optional[AsyncIOMotorDatabase] = None


class MongoDBConnection:
    """MongoDB connection manager with connection pooling and retry logic"""

    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect(cls) -> AsyncIOMotorDatabase:
        """
        Initialize MongoDB connection with retry logic and connection pooling
        """
        if cls._db is not None:
            logger.info("Using existing MongoDB connection")
            return cls._db

        retry_attempt = 0
        last_error = None

        while retry_attempt < settings.MONGO_RETRY_ATTEMPTS:
            try:
                logger.info(
                    f"Attempting to connect to MongoDB "
                    f"(Attempt {retry_attempt + 1}/{settings.MONGO_RETRY_ATTEMPTS})"
                )

                # Create client with connection pooling and timeout settings
                cls._client = AsyncIOMotorClient(
                    settings.MONGODB_URL,
                    maxPoolSize=settings.MAX_POOL_SIZE,
                    minPoolSize=settings.MIN_POOL_SIZE,
                    maxIdleTimeMS=settings.MAX_IDLE_TIME_MS,
                    connectTimeoutMS=settings.CONNECT_TIMEOUT_MS,
                    socketTimeoutMS=settings.SOCKET_TIMEOUT_MS,
                    serverSelectionTimeoutMS=settings.SERVER_SELECTION_TIMEOUT_MS,
                    retryWrites=True,
                    waitQueueTimeoutMS=10000,
                )

                # Select database
                cls._db = cls._client[settings.DATABASE_NAME]

                # Test connection with ping
                await cls._client.admin.command("ping")
                logger.info("✓ MongoDB connected successfully")

                # Create indices
                await cls._create_indices()

                global mongodb_client, mongodb_db
                mongodb_client = cls._client
                mongodb_db = cls._db

                return cls._db

            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                last_error = e
                retry_attempt += 1

                if retry_attempt < settings.MONGO_RETRY_ATTEMPTS:
                    wait_time = settings.MONGO_RETRY_DELAY_MS / 1000
                    logger.warning(
                        f"MongoDB connection failed: {e}. "
                        f"Retrying in {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(
                        f"✗ Failed to connect to MongoDB after "
                        f"{settings.MONGO_RETRY_ATTEMPTS} attempts"
                    )

            except Exception as e:
                logger.error(f"✗ Unexpected error connecting to MongoDB: {e}")
                raise

        # All retries failed
        raise ConnectionFailure(
            f"Could not connect to MongoDB after {settings.MONGO_RETRY_ATTEMPTS} "
            f"attempts. Last error: {last_error}"
        )

    @classmethod
    async def _create_indices(cls) -> None:
        """Create database indices for better performance"""
        try:
            # Create indices for users collection
            users_collection = cls._db["users"]
            await users_collection.create_index("email", unique=True)
            logger.info("✓ Database indices created successfully")
        except Exception as e:
            logger.warning(f"Failed to create indices: {e}")

    @classmethod
    async def disconnect(cls) -> None:
        """Close MongoDB connection"""
        if cls._client:
            try:
                cls._client.close()
                logger.info("✓ MongoDB connection closed")
            except Exception as e:
                logger.error(f"Error closing MongoDB connection: {e}")
            finally:
                cls._client = None
                cls._db = None

                global mongodb_client, mongodb_db
                mongodb_client = None
                mongodb_db = None


async def get_mongo_db() -> AsyncIOMotorDatabase:
    """
    Dependency for FastAPI - Get MongoDB database
    
    Returns:
        AsyncIOMotorDatabase: MongoDB database instance
        
    Raises:
        ConnectionFailure: If unable to connect to MongoDB
    """
    global mongodb_db
    
    if mongodb_db is None:
        raise ConnectionFailure("MongoDB connection not initialized. Call connect() first.")
    
    return mongodb_db


# ==================== Database Manager ====================
class Database:
    """Unified database interface"""

    @staticmethod
    async def connect() -> None:
        """Initialize database connections"""
        try:
            await MongoDBConnection.connect()
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    @staticmethod
    async def disconnect() -> None:
        """Close database connections"""
        await MongoDBConnection.disconnect()
