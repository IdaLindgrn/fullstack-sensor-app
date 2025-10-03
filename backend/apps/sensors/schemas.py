from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class SensorCreate(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100, description="Sensor identifier"
    )
    model: str = Field(
        ..., min_length=1, max_length=100, description="Sensor model name"
    )
    description: Optional[str] = Field(None, description="Optional sensor description")


class SensorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class SensorOut(BaseModel):
    id: int
    name: str
    model: str
    description: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReadingCreate(BaseModel):
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity percentage")
    timestamp: datetime = Field(..., description="Reading timestamp")


class ReadingOut(BaseModel):
    id: int
    sensor_id: int
    temperature: float
    humidity: float
    timestamp: datetime
    created_at: datetime
