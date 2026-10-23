from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.station import ChargerResponse, ChargerCreate, ChargerUpdateStatus, ChargerUpdatePrice
from app.db.models import User
from app.controllers.station_controller import StationController, AdminController
from app.routers.deps import get_station_controller, get_admin_controller, get_current_admin

router = APIRouter(tags=["Chargers"])

@router.get("/stations/{station_id}/chargers", response_model=List[ChargerResponse])
def get_station_chargers(
    station_id: int,
    controller: StationController = Depends(get_station_controller)
):
    return controller.get_station_chargers(station_id)

@router.post("/stations/{station_id}/chargers", response_model=ChargerResponse, status_code=status.HTTP_201_CREATED)
def add_charger_to_station(
    station_id: int,
    charger_in: ChargerCreate,
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    return admin_ctrl.add_charger(
        station_id=station_id,
        charger_type=charger_in.type,
        connector_type=charger_in.connector_type,
        power_kw=charger_in.power_kw,
        price_per_unit=charger_in.price_per_unit,
        status_val=charger_in.status or "Available"
    )

@router.patch("/chargers/{charger_id}/status", response_model=ChargerResponse)
def update_charger_status(
    charger_id: int,
    update_data: ChargerUpdateStatus,
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    return admin_ctrl.update_charger_status(charger_id, update_data.status)

@router.patch("/chargers/{charger_id}/pricing", response_model=ChargerResponse)
def update_charger_pricing(
    charger_id: int,
    pricing_data: ChargerUpdatePrice,
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    return admin_ctrl.update_charger_pricing(charger_id, pricing_data.price_per_unit)

@router.delete("/chargers/{charger_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_charger(
    charger_id: int,
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    admin_ctrl.delete_charger(charger_id)
    return None
