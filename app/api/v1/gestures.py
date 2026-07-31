from fastapi import APIRouter
from app.services import gesture_service

router = APIRouter()

@router.post("/")
def process_gesture(data: dict):
    return gesture_service.process_gesture_input(data)
