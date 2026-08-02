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

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_standard(image_bytes: bytes) -> StreamingResponse:
    subject_image = extract_subject(image_bytes)
    
    img_io = io.BytesIO()
    subject_image.save(img_io, format="PNG")
    img_io.seek(0)
    
    return StreamingResponse(img_io, media_type="image/png")

def process_deep(image_bytes: bytes) -> StreamingResponse:
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
    
    return StreamingResponse(img_io, media_type="image/png")

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
