from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
