from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StyleCreate(BaseModel):
    name: str
    slug: str
    prompt: str
    preview_url: Optional[str] = None

class StyleRead(BaseModel):
    id: int
    name: str
    slug: str
    prompt: str
    preview_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
