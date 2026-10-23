from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.db.models import Payment, Notification, ChargingSession, Booking, User
from app.repositories.base import BaseRepository

class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, db: Session):
        super().__init__(Payment, db)

    def get_by_session_id(self, session_id: int) -> Optional[Payment]:
        return self.db.query(Payment).filter(Payment.session_id == session_id).first()

    def get_by_transaction_id(self, transaction_id: str) -> Optional[Payment]:
        return self.db.query(Payment).filter(Payment.transaction_id == transaction_id).first()

    def get_user_payments(self, user_id: int) -> List[Payment]:
        return (
            self.db.query(Payment)
            .join(ChargingSession, Payment.session_id == ChargingSession.id)
            .join(Booking, ChargingSession.booking_id == Booking.id)
            .filter(Booking.user_id == user_id)
            .order_by(Payment.created_at.desc())
            .all()
        )

    def get_with_full_details(self, payment_id: int) -> Optional[Payment]:
        return (
            self.db.query(Payment)
            .options(
                joinedload(Payment.session)
                .joinedload(ChargingSession.booking)
                .joinedload(Booking.user),
                joinedload(Payment.session)
                .joinedload(ChargingSession.booking)
                .joinedload(Booking.charger)
            )
            .filter(Payment.id == payment_id)
            .first()
        )


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, db: Session):
        super().__init__(Notification, db)

    def get_user_notifications(self, user_id: int, limit: int = 50) -> List[Notification]:
        return (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.timestamp.desc())
            .limit(limit)
            .all()
        )

    def mark_as_read(self, notification_id: int, user_id: int) -> Optional[Notification]:
        notification = (
            self.db.query(Notification)
            .filter(Notification.id == notification_id, Notification.user_id == user_id)
            .first()
        )
        if notification:
            notification.is_read = True
            self.db.commit()
            self.db.refresh(notification)
        return notification

    def mark_all_as_read(self, user_id: int) -> int:
        count = (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read == False)
            .update({"is_read": True})
        )
        self.db.commit()
        return count
