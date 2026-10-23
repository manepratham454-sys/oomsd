"""
Payment Controller
Coordinates billing requests, strategy delegation, and invoicing.
"""

from typing import List, Dict, Any, Optional
from app.services.payment.payment_service import PaymentService
from app.db.models import Payment

class PaymentController:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def process_payment(self, session_id: int, user_id: int, payment_mode: str, details: Optional[Dict[str, Any]] = None) -> Payment:
        return self.payment_service.process_payment(
            session_id=session_id,
            user_id=user_id,
            payment_mode=payment_mode,
            details=details
        )

    def get_user_payments(self, user_id: int) -> List[Payment]:
        return self.payment_service.get_user_payments(user_id)

    def get_invoice(self, payment_id: int, user_id: int, is_admin: bool = False) -> Dict[str, Any]:
        return self.payment_service.get_invoice(payment_id=payment_id, user_id=user_id, is_admin=is_admin)
