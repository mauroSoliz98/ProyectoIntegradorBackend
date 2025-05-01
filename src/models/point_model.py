from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Severity(str, Enum):
    alto = "alto"
    medio = "medio"
    bajo = "bajo"

class DisasterType(str, Enum):
    Incendio = "Incendio"
    Inundación = "Inundación"
    Deslizamiento = "Deslizamiento"

class RequestPoint(BaseModel):
    description: str
    latitude: float
    longitude: float
    disaster_type: DisasterType
    severity: Severity
    address: Optional[str] = None
    created_by_profile_id: UUID  

class ResponsePoint(BaseModel):
    id: UUID
    description: str
    latitude: float
    longitude: float
    disaster_type: DisasterType
    severity: Severity
    address: Optional[str]
    created_at: datetime
    created_by_profile_id: UUID

    '''
    class Config:
        orm_mode = True
    '''