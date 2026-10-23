from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class SessionStartRequest(BaseModel):
    booking_id: int

class SessionStopRequest(BaseModel):
    custom_units: Optional[float] = None

class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    booking_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    units_consumed: float
    total_cost: float
    status: str

    # Contextual data
    charger_id: Optional[int] = None
    charger_type: Optional[str] = None
    power_kw: Optional[float] = None
    price_per_unit: Optional[float] = None
    station_name: Optional[str] = None
    vehicle_reg_no: Optional[str] = None
    payment_status: Optional[str] = None
    payment_id: Optional[int] = None
