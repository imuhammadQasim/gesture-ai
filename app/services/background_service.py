import io
import os
import zipfile
import logging
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from fastapi.responses import StreamingResponse
import threading
from app.ai.background_removal.rembg import extract_subject, build_dual_shadow, composite
from app.core.config import settings
from app.services.cloudinary_service import cloudinary_service

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_standard(image_bytes: bytes, filename: str = None) -> dict:
    subject_image = extract_subject(image_bytes)
    
    img_io = io.BytesIO()
    subject_image.save(img_io, format="PNG")
    img_io.seek(0)
    
    upload_response = cloudinary_service.upload_image(
        file_obj=img_io, 
        user_id="test_user", # Using test_user for now until auth is added
        module_name="background_removal",
        filename=filename
    )
    
    return {
        "message": "Background removed successfully",
        "url": upload_response.get("secure_url"),
        "public_id": upload_response.get("public_id")
    }

def process_deep(image_bytes: bytes, filename: str = None) -> dict:
    subject = extract_subject(image_bytes)
    shadow = build_dual_shadow(subject)
    
    # White background for compositing by default, or transparent?
    # Usually users want transparent for standard, and maybe white for deep if we composite.
    # We will composite onto a transparent or white bg. Let's use a solid white background as per rembg.py default.
    background = Image.new("RGBA", subject.size, (255, 255, 255, 255))
    result = composite(subject, shadow, background)
    
    img_io = io.BytesIO()
    result.save(img_io, format="PNG")
    img_io.seek(0)
    
    upload_response = cloudinary_service.upload_image(
        file_obj=img_io, 
        user_id="test_user", 
        module_name="background_removal",
        filename=filename
    )
    
    return {
        "message": "Background removed (deep) successfully",
        "url": upload_response.get("secure_url"),
        "public_id": upload_response.get("public_id")
    }

def _process_single_image(image_bytes: bytes, filename: str, output_dir: str):
    
    thread_name = threading.current_thread().name
    logger.info(f"[{thread_name}] Starting background removal for image: {filename}")
    try:
        subject_image = extract_subject(image_bytes)
        output_path = os.path.join(output_dir, f"no_bg_{filename}")
        if output_path.lower().endswith(('.jpg', '.jpeg')):
             subject_image = subject_image.convert("RGB")
        subject_image.save(output_path)
        logger.info(f"[{thread_name}] Successfully processed and saved image: {filename}")
    except Exception as e:
        logger.error(f"[{thread_name}] Error processing image {filename}: {e}")

def process_bulk_images(zip_bytes: bytes, output_dir: str):
    logger.info("Starting bulk image processing...")
    os.makedirs(output_dir, exist_ok=True)
    
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        image_files = [f for f in z.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Limit the number of images to max allowed
        image_files = image_files[:settings.MAX_BULK_IMAGES]
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            for filename in image_files:
                img_data = z.read(filename)
                executor.submit(_process_single_image, img_data, os.path.basename(filename), output_dir)
                
    logger.info("Bulk image processing task dispatched.")
