from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.payment import PaymentProcessRequest, PaymentResponse, InvoiceResponse
from app.db.models import User
from app.controllers.payment_controller import PaymentController
from app.routers.deps import get_payment_controller, get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def process_payment(
    payment_in: PaymentProcessRequest,
    current_user: User = Depends(get_current_user),
    controller: PaymentController = Depends(get_payment_controller)
):
    details = {
        "upi_id": payment_in.upi_id,
        "card_number": payment_in.card_number,
        "card_expiry": payment_in.card_expiry,
        "card_cvv": payment_in.card_cvv,
        "wallet_provider": payment_in.wallet_provider,
    }
    return controller.process_payment(
        session_id=payment_in.session_id,
        user_id=current_user.id,
        payment_mode=payment_in.payment_mode,
        details=details
    )

@router.get("/my", response_model=List[PaymentResponse])
def get_my_payments(
    current_user: User = Depends(get_current_user),
    controller: PaymentController = Depends(get_payment_controller)
):
    return controller.get_user_payments(current_user.id)

@router.get("/{payment_id}/invoice", response_model=InvoiceResponse)
def get_invoice(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    controller: PaymentController = Depends(get_payment_controller)
):
    is_admin = (current_user.role == "ADMIN")
    return controller.get_invoice(payment_id=payment_id, user_id=current_user.id, is_admin=is_admin)
