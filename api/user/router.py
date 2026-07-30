"""User routes."""
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.user.schemas import UserCreate, UserResponse, UserUpdate
from api.user.service import UserService
from core.database import get_mongo_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    existing_user = await UserService.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await UserService.create_user(db, user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    try:
        user = await UserService.get_user_by_id(db, user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user id")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    return await UserService.get_all_users(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    try:
        user = await UserService.update_user(db, user_id, user_data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user id")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    try:
        success = await UserService.delete_user(db, user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user id")

    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
