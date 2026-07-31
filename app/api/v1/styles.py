from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.core.db import get_session
from app.schemas.style import StyleCreate, StyleRead
from app.services import style_service

router = APIRouter()

@router.post("/", response_model=StyleRead)
def create_style(style_in: StyleCreate, session: Session = Depends(get_session)):
    return style_service.create_style(session=session, style_in=style_in)

@router.get("/", response_model=List[StyleRead])
def get_styles(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return style_service.get_styles(session=session, skip=skip, limit=limit)
