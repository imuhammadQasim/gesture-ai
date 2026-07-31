import cloudinary
from app.core.config import settings

def init_cloudinary():
    """
    Initialize Cloudinary configuration from environment variables.
    You can call this during app startup or it can be initialized automatically if the CLOUDINARY_URL env var is set.
    """
    # If CLOUDINARY_URL is available, it gets configured automatically.
    # Otherwise, we use individual parameters.
    if settings.CLOUDINARY_URL:
        cloudinary.config() # Automatically picks up CLOUDINARY_URL from env if set globally
    elif settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )
