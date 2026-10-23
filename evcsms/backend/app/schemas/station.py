from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class ChargerCreate(BaseModel):
    station_id: int
    type: str = Field(..., description="AC or DC Fast")
    connector_type: str = Field("CCS2", description="CCS2, Type 2, CHAdeMO")
    power_kw: float = Field(50.0, gt=0)
    price_per_unit: float = Field(15.0, gt=0)
    status: Optional[str] = Field("Available", pattern="^(Available|Busy|Reserved|Offline)$")

class ChargerUpdateStatus(BaseModel):
    status: str = Field(..., pattern="^(Available|Busy|Reserved|Offline)$")

class ChargerUpdatePrice(BaseModel):
    price_per_unit: float = Field(..., gt=0)

class ChargerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    station_id: int
    type: str
    connector_type: str
    power_kw: float
    status: str
    price_per_unit: float

class StationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    country: str = Field("India", max_length=100)
    latitude: float
    longitude: float
    address: Optional[str] = None

class StationUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None

class StationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float
    address: Optional[str]
    total_chargers: int = 0
    available_chargers: int = 0
    distance_km: Optional[float] = None
    min_price: Optional[float] = None
    charger_types: List[str] = []

class StationDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float
    address: Optional[str]
    chargers: List[ChargerResponse] = []
