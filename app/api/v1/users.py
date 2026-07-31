from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.core.db import get_session
from app.schemas.user import UserCreate, UserRead
from app.services import user_service

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    return user_service.create_user(session=session, user_in=user_in)

@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return user_service.get_users(session=session, skip=skip, limit=limit)
