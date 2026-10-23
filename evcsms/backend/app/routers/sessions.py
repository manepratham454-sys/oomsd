from fastapi import APIRouter, Depends, status
from typing import List, Optional
from app.schemas.session import SessionStartRequest, SessionStopRequest, SessionResponse
from app.db.models import User, ChargingSession
from app.controllers.session_controller import SessionController
from app.repositories.session_repository import SessionRepository
from app.routers.deps import get_session_controller, get_session_repo, get_current_user

router = APIRouter(prefix="/sessions", tags=["Charging Sessions"])

def serialize_session(s: ChargingSession) -> dict:
    booking = s.booking
    charger = booking.charger if booking else None
    station = charger.station if charger else None
    vehicle = booking.vehicle if booking else None
    payment = s.payment

    return {
        "id": s.id,
        "booking_id": s.booking_id,
        "start_time": s.start_time,
        "end_time": s.end_time,
        "units_consumed": s.units_consumed,
        "total_cost": s.total_cost,
        "status": s.status,
        "charger_id": charger.id if charger else None,
        "charger_type": charger.type if charger else None,
        "power_kw": charger.power_kw if charger else None,
        "price_per_unit": charger.price_per_unit if charger else None,
        "station_name": station.name if station else None,
        "vehicle_reg_no": vehicle.reg_no if vehicle else None,
        "payment_status": payment.status if payment else None,
        "payment_id": payment.id if payment else None,
    }

@router.post("/start", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def start_session(
    payload: SessionStartRequest,
    current_user: User = Depends(get_current_user),
    controller: SessionController = Depends(get_session_controller)
):
    session = controller.start_session(booking_id=payload.booking_id, user_id=current_user.id)
    return serialize_session(session)

@router.post("/{session_id}/stop", response_model=SessionResponse)
def stop_session(
    session_id: int,
    payload: Optional[SessionStopRequest] = None,
    current_user: User = Depends(get_current_user),
    controller: SessionController = Depends(get_session_controller)
):
    custom_units = payload.custom_units if payload else None
    session = controller.stop_session(session_id=session_id, user_id=current_user.id, custom_units=custom_units)
    return serialize_session(session)

@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    controller: SessionController = Depends(get_session_controller)
):
    session = controller.get_session(session_id)
    return serialize_session(session)

@router.get("/my/active", response_model=List[SessionResponse])
def get_my_active_sessions(
    current_user: User = Depends(get_current_user),
    session_repo: SessionRepository = Depends(get_session_repo)
):
    sessions = session_repo.get_active_sessions_for_user(current_user.id)
    return [serialize_session(s) for s in sessions]
