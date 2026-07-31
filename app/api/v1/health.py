from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def check_health():
    return {"message": "Not implemented yet"}
