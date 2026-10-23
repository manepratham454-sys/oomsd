from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone_no: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=6)
    role: Optional[str] = Field("EV_OWNER", pattern="^(EV_OWNER|ADMIN)$")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    name: str
    email: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone_no: Optional[str]
    role: str
    created_at: Optional[datetime]
