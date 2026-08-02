import os
import uuid
from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from app.services import background_service

router = APIRouter()

@router.post("/standard")
async def remove_background_standard(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return background_service.process_standard(image_bytes, file.filename)

@router.post("/deep")
async def remove_background_deep(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return background_service.process_deep(image_bytes, file.filename)

@router.post("/bulk")
async def remove_background_bulk(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed for bulk upload.")
    
    zip_bytes = await file.read()
    task_id = str(uuid.uuid4())
    output_dir = os.path.join("outputs", f"bulk_{task_id}")
    
    background_tasks.add_task(background_service.process_bulk_images, zip_bytes, output_dir)
    
    return {"message": "Bulk processing started", "task_id": task_id, "output_dir": output_dir}
