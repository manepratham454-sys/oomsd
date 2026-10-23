from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class BookingCreate(BaseModel):
    charger_id: int
    vehicle_id: Optional[int] = None
    start_time: datetime
    end_time: datetime

class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    charger_id: int
    vehicle_id: Optional[int]
    start_time: datetime
    end_time: datetime
    status: str
    created_at: Optional[datetime]

    # Additional contextual fields for rich UI
    charger_type: Optional[str] = None
    connector_type: Optional[str] = None
    price_per_unit: Optional[float] = None
    station_name: Optional[str] = None
    station_city: Optional[str] = None
    vehicle_reg_no: Optional[str] = None
    session_id: Optional[int] = None
    session_status: Optional[str] = None
