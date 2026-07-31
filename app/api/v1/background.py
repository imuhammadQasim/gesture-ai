from fastapi import APIRouter
from app.services import background_service

router = APIRouter()

@router.post("/remove")
def remove_background(data: dict):
    return background_service.process_background_removal(data)
