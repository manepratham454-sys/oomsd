"""
Booking Controller
GRASP Principle Applied:
- Controller Pattern: BookingController serves as the first object beyond the UI/Router layer
  that coordinates and controls all system operations related to bookings (creation, conflicts, cancellation, history).
"""

from typing import List, Optional
from datetime import datetime
from app.services.booking_service import BookingService
from app.db.models import Booking

class BookingController:
    """
    GRASP Controller Pattern:
    Coordinates booking lifecycle operations between presentation routers and business services.
    """
    def __init__(self, booking_service: BookingService):
        self.booking_service = booking_service

    def create_booking(
        self,
        user_id: int,
        charger_id: int,
        start_time: datetime,
        end_time: datetime,
        vehicle_id: Optional[int] = None,
    ) -> Booking:
        return self.booking_service.create_booking(
            user_id=user_id,
            charger_id=charger_id,
            start_time=start_time,
            end_time=end_time,
            vehicle_id=vehicle_id
        )

    def get_user_bookings(self, user_id: int) -> List[Booking]:
        return self.booking_service.get_user_bookings(user_id)

    def cancel_booking(self, booking_id: int, user_id: int) -> Booking:
        return self.booking_service.cancel_booking(booking_id, user_id)
