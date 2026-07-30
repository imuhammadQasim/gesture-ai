"""User service backed by MongoDB."""
from datetime import datetime, timezone
from typing import List, Optional

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from api.user.schemas import UserCreate, UserUpdate


class UserService:
    """MongoDB CRUD operations for users."""

    @staticmethod
    def _collection(db: AsyncIOMotorDatabase):
        return db["users"]

    @staticmethod
    def _serialize_user(user: dict) -> dict:
        user["id"] = str(user.pop("_id"))
        return user

    @staticmethod
    def _object_id(user_id: str) -> ObjectId:
        try:
            return ObjectId(user_id)
        except InvalidId as exc:
            raise ValueError("Invalid user id") from exc

    @classmethod
    async def create_user(cls, db: AsyncIOMotorDatabase, user_data: UserCreate) -> dict:
        now = datetime.now(timezone.utc)
        new_user = {
            **user_data.model_dump(),
            "created_at": now,
            "updated_at": None,
        }
        result = await cls._collection(db).insert_one(new_user)
        new_user["_id"] = result.inserted_id
        return cls._serialize_user(new_user)

    @classmethod
    async def get_user_by_id(cls, db: AsyncIOMotorDatabase, user_id: str) -> Optional[dict]:
        user = await cls._collection(db).find_one({"_id": cls._object_id(user_id)})
        return cls._serialize_user(user) if user else None

    @classmethod
    async def get_user_by_email(cls, db: AsyncIOMotorDatabase, email: str) -> Optional[dict]:
        user = await cls._collection(db).find_one({"email": email})
        return cls._serialize_user(user) if user else None

    @classmethod
    async def get_all_users(
        cls,
        db: AsyncIOMotorDatabase,
        skip: int = 0,
        limit: int = 100,
    ) -> List[dict]:
        cursor = cls._collection(db).find().skip(skip).limit(limit)
        users = await cursor.to_list(length=limit)
        return [cls._serialize_user(user) for user in users]

    @classmethod
    async def update_user(
        cls,
        db: AsyncIOMotorDatabase,
        user_id: str,
        user_data: UserUpdate,
    ) -> Optional[dict]:
        update_data = user_data.model_dump(exclude_unset=True)
        if not update_data:
            return await cls.get_user_by_id(db, user_id)

        update_data["updated_at"] = datetime.now(timezone.utc)
        user = await cls._collection(db).find_one_and_update(
            {"_id": cls._object_id(user_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )
        return cls._serialize_user(user) if user else None

    @classmethod
    async def delete_user(cls, db: AsyncIOMotorDatabase, user_id: str) -> bool:
        result = await cls._collection(db).delete_one({"_id": cls._object_id(user_id)})
        return result.deleted_count == 1
