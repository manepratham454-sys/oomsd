from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.booking import BookingCreate, BookingResponse
from app.db.models import User, Booking
from app.controllers.booking_controller import BookingController
from app.routers.deps import get_booking_controller, get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

def serialize_booking(b: Booking) -> dict:
    charger = b.charger
    station = charger.station if charger else None
    vehicle = b.vehicle
    session = b.session

    return {
        "id": b.id,
        "user_id": b.user_id,
        "charger_id": b.charger_id,
        "vehicle_id": b.vehicle_id,
        "start_time": b.start_time,
        "end_time": b.end_time,
        "status": b.status,
        "created_at": b.created_at,
        "charger_type": charger.type if charger else None,
        "connector_type": charger.connector_type if charger else None,
        "price_per_unit": charger.price_per_unit if charger else None,
        "station_name": station.name if station else None,
        "station_city": station.city if station else None,
        "vehicle_reg_no": vehicle.reg_no if vehicle else None,
        "session_id": session.id if session else None,
        "session_status": session.status if session else None,
    }

@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingCreate,
    current_user: User = Depends(get_current_user),
    controller: BookingController = Depends(get_booking_controller)
):
    saved_booking = controller.create_booking(
        user_id=current_user.id,
        charger_id=booking_in.charger_id,
        start_time=booking_in.start_time,
        end_time=booking_in.end_time,
        vehicle_id=booking_in.vehicle_id
    )
    return serialize_booking(saved_booking)

@router.get("/my", response_model=List[BookingResponse])
def get_my_bookings(
    current_user: User = Depends(get_current_user),
    controller: BookingController = Depends(get_booking_controller)
):
    bookings = controller.get_user_bookings(current_user.id)
    return [serialize_booking(b) for b in bookings]

@router.delete("/{booking_id}", response_model=BookingResponse)
def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    controller: BookingController = Depends(get_booking_controller)
):
    cancelled = controller.cancel_booking(booking_id, current_user.id)
    return serialize_booking(cancelled)
