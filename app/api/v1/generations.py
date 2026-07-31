from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.core.db import get_session
from app.schemas.generation import GenerationCreate, GenerationRead
from app.services import generation_service

router = APIRouter()

@router.post("/", response_model=GenerationRead)
def create_generation(generation_in: GenerationCreate, session: Session = Depends(get_session)):
    return generation_service.create_generation(session=session, generation_in=generation_in)

@router.get("/", response_model=List[GenerationRead])
def get_generations(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return generation_service.get_generations(session=session, skip=skip, limit=limit)
