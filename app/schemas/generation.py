from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GenerationCreate(BaseModel):
    user_id: int
    style_id: int
    type: str
    input_url: Optional[str] = None

class GenerationRead(BaseModel):
    id: int
    user_id: int
    style_id: int
    type: str
    input_url: Optional[str] = None
    output_url: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
