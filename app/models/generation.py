from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Generation(SQLModel, table=True):
    __tablename__ = "generations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    style_id: int = Field(foreign_key="styles.id", index=True)
    type: str # e.g., 'face_style', 'background_replacement'
    input_url: Optional[str] = None
    output_url: Optional[str] = None
    status: str = Field(default="pending") # pending, processing, completed, failed
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
