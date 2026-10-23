"""
Booking Service Layer
Applies:
- Interface Segregation Principle (ISP): Implements IBookingService
- GRASP Controller collaboration: Dispatches domain logic to Booking and Charger entities
- Conflict resolution: Rejects overlapping slots for the same charger
- Vehicle connector compatibility validation
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.interfaces.services import IBookingService
from app.repositories.booking_repository import BookingRepository
from app.repositories.charger_repository import ChargerRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.services.notification_service import NotificationService
from app.db.models import Booking

class BookingService(IBookingService):
    def __init__(
        self,
        booking_repo: BookingRepository,
        charger_repo: ChargerRepository,
        vehicle_repo: VehicleRepository,
        notification_service: NotificationService,
    ):
        self.booking_repo = booking_repo
        self.charger_repo = charger_repo
        self.vehicle_repo = vehicle_repo
        self.notification_service = notification_service

    def check_slot_conflict(
        self, charger_id: int, start_time: datetime, end_time: datetime, exclude_booking_id: Optional[int] = None
    ) -> bool:
        """Returns True if there is a slot conflict (overlap), False otherwise."""
        conflicts = self.booking_repo.get_overlapping_bookings(
            charger_id=charger_id,
            start_time=start_time,
            end_time=end_time,
            exclude_booking_id=exclude_booking_id
        )
        return len(conflicts) > 0

    def create_booking(
        self,
        user_id: int,
        charger_id: int,
        start_time: datetime,
        end_time: datetime,
        vehicle_id: Optional[int] = None,
    ) -> Booking:
        # Validate time ordering
        if start_time >= end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking start time must be strictly before end time."
            )

        # Check charger existence and status
        charger = self.charger_repo.get_by_id(charger_id)
        if not charger:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charger not found.")

        if charger.status == "Offline":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot book an offline charger.")

        # Validate connector compatibility with vehicle (if vehicle selected)
        if vehicle_id:
            vehicle = self.vehicle_repo.get_by_id(vehicle_id)
            if not vehicle:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Selected vehicle not found.")
            if vehicle.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own the selected vehicle.")

            # Validate connector compatibility
            if vehicle.connector_type.strip().lower() != charger.connector_type.strip().lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Connector mismatch! Vehicle '{vehicle.reg_no}' requires '{vehicle.connector_type}' "
                        f"connector, but Charger #{charger.id} provides '{charger.connector_type}'."
                    ),
                )

        # Reject overlapping slots
        if self.check_slot_conflict(charger_id, start_time, end_time):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The requested time slot conflicts with an existing booking for this charger."
            )

        # Step in Booking Flow: User creates booking -> Charger reserved -> Booking confirmed -> Notification sent
        booking = Booking(
            user_id=user_id,
            charger_id=charger_id,
            vehicle_id=vehicle_id,
            start_time=start_time,
            end_time=end_time,
            status="Confirmed",
            reminder_sent=False,
            created_at=datetime.now(timezone.utc)
        )
        saved_booking = self.booking_repo.create(booking)

        # Reserve charger status if booking is starting soon or immediate
        # (or mark as Reserved to signal availability holds)
        if charger.status == "Available":
            self.charger_repo.update_status(charger_id, "Reserved")

        # Send confirmation notification
        self.notification_service.send_notification(
            user_id=user_id,
            message=(
                f"Booking #{saved_booking.id} confirmed for Charger #{charger_id} at "
                f"{start_time.strftime('%Y-%m-%d %H:%M UTC')}."
            ),
            notification_type="BOOKING_CONFIRMED"
        )

        return saved_booking

    def get_user_bookings(self, user_id: int) -> List[Booking]:
        return self.booking_repo.get_by_user_id(user_id)

    def cancel_booking(self, booking_id: int, user_id: int) -> Booking:
        booking = self.booking_repo.get_booking_detail(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found.")

        if booking.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to cancel this booking.")

        if booking.status in ["Completed", "Expired"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot cancel a booking in status {booking.status}.")

        if booking.session and booking.session.status == "Active":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot cancel booking while charging session is active.")

        booking.status = "Cancelled"
        saved_booking = self.booking_repo.update(booking)

        # Release charger back to Available
        if booking.charger and booking.charger.status in ["Reserved", "Busy"]:
            # Check if there is another confirmed booking starting right now
            other_active = self.booking_repo.get_overlapping_bookings(
                charger_id=booking.charger_id,
                start_time=datetime.now(timezone.utc),
                end_time=datetime.now(timezone.utc),
                exclude_booking_id=booking.id
            )
            if not other_active:
                self.charger_repo.update_status(booking.charger_id, "Available")

        # Notification
        self.notification_service.send_notification(
            user_id=user_id,
            message=f"Booking #{booking_id} has been successfully cancelled.",
            notification_type="BOOKING_CANCELLED"
        )

        return saved_booking
