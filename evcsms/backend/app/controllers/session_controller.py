"""
Session Controller
Coordinates telemetry operations, charging cycles, and energy computation requests.
"""

from typing import Optional
from app.services.session_service import SessionService
from app.db.models import ChargingSession

class SessionController:
    def __init__(self, session_service: SessionService):
        self.session_service = session_service

    def start_session(self, booking_id: int, user_id: int) -> ChargingSession:
        return self.session_service.start_session(booking_id=booking_id, user_id=user_id)

    def stop_session(self, session_id: int, user_id: int, custom_units: Optional[float] = None) -> ChargingSession:
        return self.session_service.stop_session(session_id=session_id, user_id=user_id, custom_units=custom_units)

    def get_session(self, session_id: int) -> ChargingSession:
        return self.session_service.get_session(session_id)
