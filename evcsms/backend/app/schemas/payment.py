from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class PaymentProcessRequest(BaseModel):
    session_id: int
    payment_mode: str = Field(..., pattern="^(UPI|Card|Wallet)$", description="Payment Mode: UPI, Card, Wallet")
    upi_id: Optional[str] = None
    card_number: Optional[str] = None
    card_expiry: Optional[str] = None
    card_cvv: Optional[str] = None
    wallet_provider: Optional[str] = None

class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    amount: float
    payment_mode: str
    status: str
    transaction_id: str
    created_at: Optional[datetime]

class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    invoice_number: str
    transaction_id: str
    payment_id: int
    session_id: int
    booking_id: int
    user_name: str
    user_email: str
    station_name: str
    station_address: Optional[str]
    charger_type: str
    power_kw: float
    units_consumed: float
    price_per_unit: float
    amount: float
    tax_amount: float
    total_payable: float
    payment_mode: str
    status: str
    start_time: datetime
    end_time: Optional[datetime]
    created_at: datetime
