from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class VehicleCreate(BaseModel):
    reg_no: str = Field(..., min_length=4, max_length=50)
    battery_capacity: float = Field(..., gt=0, description="Battery capacity in kWh")
    connector_type: str = Field(..., description="e.g. CCS2, Type 2, CHAdeMO, GB/T")

class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reg_no: str
    battery_capacity: float
    connector_type: str
    user_id: int
