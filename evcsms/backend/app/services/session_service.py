"""
Session Service Layer
GRASP Principles Applied:
- Creator: Uses Booking entity logic to create ChargingSession
- Information Expert: Delegates energy metering and billing calculations to ChargingSession
- Updates hardware charger operational states (Busy -> Available)
"""

from typing import Optional, List
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from app.interfaces.services import ISessionService
from app.repositories.session_repository import SessionRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.charger_repository import ChargerRepository
from app.services.notification_service import NotificationService
from app.db.models import ChargingSession
from app.domain.entities import Booking as DomainBooking, ChargingSession as DomainSession

class SessionService(ISessionService):
    def __init__(
        self,
        session_repo: SessionRepository,
        booking_repo: BookingRepository,
        charger_repo: ChargerRepository,
        notification_service: NotificationService,
    ):
        self.session_repo = session_repo
        self.booking_repo = booking_repo
        self.charger_repo = charger_repo
        self.notification_service = notification_service

    def start_session(self, booking_id: int, user_id: int) -> ChargingSession:
        booking = self.booking_repo.get_booking_detail(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found.")

        if booking.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to start session for this booking.")

        if booking.status != "Confirmed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot start session. Booking is in status '{booking.status}' (must be 'Confirmed')."
            )

        # Time window check: Allowed from 15 mins before start_time up to end_time
        # Make timestamps timezone-aware for comparison
        now = datetime.now(timezone.utc)
        start_tz = booking.start_time.replace(tzinfo=timezone.utc) if booking.start_time.tzinfo is None else booking.start_time
        end_tz = booking.end_time.replace(tzinfo=timezone.utc) if booking.end_time.tzinfo is None else booking.end_time

        grace_start = start_tz - timedelta(minutes=15)
        if now < grace_start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Too early! Charging session can only be initiated within 15 minutes of booking start time ({start_tz.strftime('%H:%M UTC')})."
            )

        if now > end_tz:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking slot has already expired. Please create a new booking."
            )

        # Check if session already exists for this booking
        existing_session = self.session_repo.get_by_booking_id(booking_id)
        if existing_session:
            if existing_session.status == "Active":
                return existing_session
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Charging session for this booking has already completed.")

        # GRASP Creator: Booking creates ChargingSession
        domain_booking = DomainBooking(
            booking_id=booking.id,
            user_id=booking.user_id,
            charger_id=booking.charger_id,
            start_time=booking.start_time,
            end_time=booking.end_time,
            status=booking.status
        )
        domain_session = domain_booking.create_session()

        db_session = ChargingSession(
            booking_id=booking.id,
            start_time=now,
            units_consumed=0.0,
            total_cost=0.0,
            status="Active"
        )
        saved_session = self.session_repo.create(db_session)

        # Set charger to Busy
        self.charger_repo.update_status(booking.charger_id, "Busy")

        # Notification
        self.notification_service.send_notification(
            user_id=user_id,
            message=f"Charging session #{saved_session.id} started on Charger #{booking.charger_id}.",
            notification_type="SESSION_STARTED"
        )

        return saved_session

    def stop_session(self, session_id: int, user_id: int, custom_units: Optional[float] = None) -> ChargingSession:
        session = self.session_repo.get_with_details(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charging session not found.")

        booking = session.booking
        if booking.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to stop this session.")

        if session.status == "Completed":
            return session

        now = datetime.now(timezone.utc)
        charger = booking.charger
        power_kw = charger.power_kw if charger else 50.0
        price_per_unit = charger.price_per_unit if charger else 15.0

        session.end_time = now

        # GRASP Information Expert: ChargingSession calculates consumed units and cost
        domain_session = DomainSession(
            session_id=session.id,
            booking_id=session.booking_id,
            start_time=session.start_time.replace(tzinfo=timezone.utc) if session.start_time.tzinfo is None else session.start_time,
            end_time=now,
            status="Active"
        )

        if custom_units is not None and custom_units > 0:
            session.units_consumed = round(custom_units, 2)
            session.total_cost = round(custom_units * price_per_unit, 2)
        else:
            domain_session.compute_energy_and_cost(charger_power_kw=power_kw, price_per_unit=price_per_unit, end_time=now)
            session.units_consumed = domain_session.units_consumed
            session.total_cost = domain_session.total_cost

        session.status = "Completed"
        booking.status = "Completed"
        self.booking_repo.update(booking)
        saved_session = self.session_repo.update(session)

        # Release charger back to Available
        if charger:
            self.charger_repo.update_status(charger.id, "Available")

        # Notification
        self.notification_service.send_notification(
            user_id=user_id,
            message=(
                f"Charging session #{saved_session.id} stopped. Consumed: {saved_session.units_consumed} kWh. "
                f"Total Amount: ₹{saved_session.total_cost:.2f}. Please proceed to payment."
            ),
            notification_type="SESSION_COMPLETED"
        )

        return saved_session

    def get_session(self, session_id: int) -> ChargingSession:
        session = self.session_repo.get_with_details(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charging session not found.")
        return session
