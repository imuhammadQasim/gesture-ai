import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Optional, Union, BinaryIO
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Cloudinary configuration
try:
    if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
        cloudinary.config( 
          cloud_name = settings.CLOUDINARY_CLOUD_NAME, 
          api_key = settings.CLOUDINARY_API_KEY, 
          api_secret = settings.CLOUDINARY_API_SECRET,
          secure = True
        )
        print("Cloudinary credentials are set",settings.CLOUDINARY_CLOUD_NAME, settings.CLOUDINARY_API_KEY, settings.CLOUDINARY_API_SECRET)
    else:
        logger.warning("Cloudinary credentials are not fully set in the environment variables.")
except Exception as e:
    logger.error(f"Error initializing Cloudinary: {e}")

class CloudinaryService:
    @staticmethod
    def upload_image(
        file_obj: Union[str, bytes, BinaryIO], 
        user_id: str = "anonymous_user", 
        module_name: str = "general", 
        filename: Optional[str] = None
    ) -> dict:
        """
        Uploads an image to Cloudinary, organizing it by user_id and module_name.
        Creates a clean folder structure: users/{user_id}/{module_name}/
        
        Args:
            file_obj: Can be a file path, bytes, or a file-like object (e.g., io.BytesIO).
            user_id: The ID of the user uploading the file (defaults to "anonymous_user").
            module_name: The module or feature (e.g., "background_removal").
            filename: Optional original filename.
            
        Returns:
            A dictionary containing Cloudinary response (e.g., 'secure_url', 'public_id').
        """
        folder_path = f"users/{user_id}/{module_name}"
        
        upload_kwargs = {
            "folder": folder_path
        }
        
        if filename:
            # Cloudinary handles file extensions separately, so we strip it for public_id
            public_id, _ = os.path.splitext(filename)
            upload_kwargs["public_id"] = public_id

        logger.info(f"Uploading image to Cloudinary folder: {folder_path}")
        response = cloudinary.uploader.upload(file_obj, **upload_kwargs)
        print("Response of the cloudinary Service Object : " , response)
        return response
        
    @staticmethod
    def delete_image(public_id: str) -> dict:
        """
        Deletes an image from Cloudinary by its public ID.
        """
        logger.info(f"Deleting image from Cloudinary with public_id: {public_id}")
        return cloudinary.uploader.destroy(public_id)

cloudinary_service = CloudinaryService()
