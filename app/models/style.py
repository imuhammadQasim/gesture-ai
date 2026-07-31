from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Style(SQLModel, table=True):
    __tablename__ = "styles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    slug: str = Field(unique=True, index=True)
    prompt: str
    preview_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
