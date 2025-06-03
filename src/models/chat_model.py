from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateMessage(BaseModel):
    profile_id: str
    content: str

class ResponseMessage(BaseModel):
    id: str
    profile_id: str
    content: str
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True