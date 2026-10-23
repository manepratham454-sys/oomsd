from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.db.models import ChargingSession, Booking, Charger, Station, Vehicle, Payment
from app.repositories.base import BaseRepository

class SessionRepository(BaseRepository[ChargingSession]):
    def __init__(self, db: Session):
        super().__init__(ChargingSession, db)

    def get_by_booking_id(self, booking_id: int) -> Optional[ChargingSession]:
        return (
            self.db.query(ChargingSession)
            .options(
                joinedload(ChargingSession.booking).joinedload(Booking.charger).joinedload(Charger.station),
                joinedload(ChargingSession.payment),
            )
            .filter(ChargingSession.booking_id == booking_id)
            .first()
        )

    def get_with_details(self, session_id: int) -> Optional[ChargingSession]:
        return (
            self.db.query(ChargingSession)
            .options(
                joinedload(ChargingSession.booking).joinedload(Booking.charger).joinedload(Charger.station),
                joinedload(ChargingSession.booking).joinedload(Booking.vehicle),
                joinedload(ChargingSession.booking).joinedload(Booking.user),
                joinedload(ChargingSession.payment),
            )
            .filter(ChargingSession.id == session_id)
            .first()
        )

    def get_active_sessions_for_user(self, user_id: int) -> List[ChargingSession]:
        return (
            self.db.query(ChargingSession)
            .join(Booking, ChargingSession.booking_id == Booking.id)
            .options(
                joinedload(ChargingSession.booking).joinedload(Booking.charger).joinedload(Charger.station),
                joinedload(ChargingSession.booking).joinedload(Booking.vehicle),
            )
            .filter(Booking.user_id == user_id, ChargingSession.status == "Active")
            .all()
        )

    def get_all_active_sessions(self) -> List[ChargingSession]:
        return self.db.query(ChargingSession).filter(ChargingSession.status == "Active").all()
