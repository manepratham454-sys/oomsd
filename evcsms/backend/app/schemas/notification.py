from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    message: str
    timestamp: datetime
    type: str
    is_read: bool

class NotificationReadResponse(BaseModel):
    id: int
    is_read: bool
