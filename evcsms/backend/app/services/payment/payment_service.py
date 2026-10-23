"""
Payment Service Layer
SOLID Principles Applied:
- Single Responsibility Principle (SRP): This service handles billing, transaction settlements,
  and invoice generation ONLY. It delegates session management to SessionService and alerts to NotificationService.
- Dependency Inversion Principle (DIP): Injected with PaymentRepository and Base Strategy abstractions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.interfaces.services import IPaymentService
from app.repositories.payment_repository import PaymentRepository
from app.repositories.session_repository import SessionRepository
from app.services.payment.strategy import PaymentStrategyFactory
from app.db.models import Payment

class PaymentService(IPaymentService):
    """
    Payment Service implementing IPaymentService.
    SRP: Handles billing, payment transactions, and invoices.
    """
    def __init__(self, payment_repo: PaymentRepository, session_repo: SessionRepository):
        self.payment_repo = payment_repo
        self.session_repo = session_repo

    def process_payment(self, session_id: int, user_id: int, payment_mode: str, details: Optional[Dict[str, Any]] = None) -> Payment:
        session = self.session_repo.get_with_details(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charging session not found.")

        # Ensure current user owns the booking for this session
        if session.booking.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to pay for this session.")

        if session.status != "Completed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot pay for an in-progress session. Stop session first.")

        # Check if already paid
        existing_payment = self.payment_repo.get_by_session_id(session_id)
        if existing_payment and existing_payment.status == "Success":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment already completed for this session.")

        # Minimum amount safeguard
        amount = max(session.total_cost, 10.0)  # Min simulated charge 10 INR

        # Retrieve strategy via Strategy Factory (OCP + LSP)
        try:
            strategy = PaymentStrategyFactory.get_strategy(payment_mode)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        # Process mock transaction
        success, txn_id, message = strategy.process_transaction(amount, details or {})

        if not success:
            failed_payment = Payment(
                session_id=session_id,
                amount=amount,
                payment_mode=payment_mode,
                status="Failed",
                transaction_id=txn_id,
                created_at=datetime.now(timezone.utc)
            )
            self.payment_repo.create(failed_payment)
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Payment transaction failed: {message}"
            )

        # Record successful payment
        if existing_payment:
            existing_payment.status = "Success"
            existing_payment.payment_mode = payment_mode
            existing_payment.transaction_id = txn_id
            existing_payment.amount = amount
            saved_payment = self.payment_repo.update(existing_payment)
        else:
            payment_obj = Payment(
                session_id=session_id,
                amount=amount,
                payment_mode=payment_mode,
                status="Success",
                transaction_id=txn_id,
                created_at=datetime.now(timezone.utc)
            )
            saved_payment = self.payment_repo.create(payment_obj)

        return saved_payment

    def get_user_payments(self, user_id: int) -> List[Payment]:
        return self.payment_repo.get_user_payments(user_id)

    def get_invoice(self, payment_id: int, user_id: int, is_admin: bool = False) -> Dict[str, Any]:
        payment = self.payment_repo.get_with_full_details(payment_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment record not found.")

        session = payment.session
        booking = session.booking
        user = booking.user

        if not is_admin and user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this invoice.")

        station = booking.charger.station
        charger = booking.charger

        base_amount = payment.amount
        gst_rate = 0.18  # 18% GST standard in India
        tax_amount = round(base_amount * (gst_rate / (1.0 + gst_rate)), 2)
        net_amount = round(base_amount - tax_amount, 2)

        return {
            "invoice_number": f"INV-{payment.id:06d}-{payment.created_at.strftime('%Y%m%d') if payment.created_at else '2026'}",
            "transaction_id": payment.transaction_id,
            "payment_id": payment.id,
            "session_id": session.id,
            "booking_id": booking.id,
            "user_name": user.name,
            "user_email": user.email,
            "station_name": station.name,
            "station_address": station.address,
            "charger_type": charger.type,
            "power_kw": charger.power_kw,
            "units_consumed": session.units_consumed,
            "price_per_unit": charger.price_per_unit,
            "amount": net_amount,
            "tax_amount": tax_amount,
            "total_payable": base_amount,
            "payment_mode": payment.payment_mode,
            "status": payment.status,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "created_at": payment.created_at or datetime.now(timezone.utc),
        }
