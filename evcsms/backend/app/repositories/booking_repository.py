from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from datetime import datetime
from app.db.models import Booking, Charger, Station, Vehicle, ChargingSession
from app.repositories.base import BaseRepository

class BookingRepository(BaseRepository[Booking]):
    def __init__(self, db: Session):
        super().__init__(Booking, db)

    def get_overlapping_bookings(
        self, charger_id: int, start_time: datetime, end_time: datetime, exclude_booking_id: Optional[int] = None
    ) -> List[Booking]:
        """
        Check for overlapping bookings on the same charger.
        Overlaps when: existing.start_time < new.end_time AND existing.end_time > new.start_time
        and status is in ('Confirmed', 'Pending')
        """
        query = self.db.query(Booking).filter(
            Booking.charger_id == charger_id,
            Booking.status.in_(["Confirmed", "Pending"]),
            Booking.start_time < end_time,
            Booking.end_time > start_time
        )
        if exclude_booking_id:
            query = query.filter(Booking.id != exclude_booking_id)
        return query.all()

    def get_by_user_id(self, user_id: int) -> List[Booking]:
        return (
            self.db.query(Booking)
            .options(
                joinedload(Booking.charger).joinedload(Charger.station),
                joinedload(Booking.vehicle),
                joinedload(Booking.session).joinedload(ChargingSession.payment),
            )
            .filter(Booking.user_id == user_id)
            .order_by(Booking.start_time.desc())
            .all()
        )

    def get_booking_detail(self, booking_id: int) -> Optional[Booking]:
        return (
            self.db.query(Booking)
            .options(
                joinedload(Booking.charger).joinedload(Charger.station),
                joinedload(Booking.vehicle),
                joinedload(Booking.session),
            )
            .filter(Booking.id == booking_id)
            .first()
        )

    def get_unclaimed_bookings(self, threshold_time: datetime) -> List[Booking]:
        """
        Bookings that started before threshold_time (e.g. 10 mins ago),
        status is 'Confirmed', and have no active session started.
        """
        return (
            self.db.query(Booking)
            .outerjoin(ChargingSession, Booking.id == ChargingSession.booking_id)
            .filter(
                Booking.status == "Confirmed",
                Booking.start_time <= threshold_time,
                ChargingSession.id == None  # No session initiated
            )
            .all()
        )

    def get_upcoming_bookings_for_reminder(self, window_start: datetime, window_end: datetime) -> List[Booking]:
        """
        Bookings starting within the reminder window (e.g. 15 min ahead) that haven't received reminder yet.
        """
        return (
            self.db.query(Booking)
            .filter(
                Booking.status == "Confirmed",
                Booking.reminder_sent == False,
                Booking.start_time >= window_start,
                Booking.start_time <= window_end
            )
            .all()
        )
