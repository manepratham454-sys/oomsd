from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from app.schemas.station import (
    StationResponse, StationDetailResponse, StationCreate, StationUpdate
)
from app.db.models import User
from app.controllers.station_controller import StationController, AdminController
from app.routers.deps import get_station_controller, get_admin_controller, get_current_admin

router = APIRouter(prefix="/stations", tags=["Stations"])

@router.get("", response_model=List[StationResponse])
def get_stations(
    city: Optional[str] = Query(None, description="Filter by station city"),
    charger_type: Optional[str] = Query(None, description="Filter by charger type: AC or DC Fast"),
    available_only: bool = Query(False, description="Show only stations with available chargers"),
    lat: Optional[float] = Query(None, description="User latitude for nearby search"),
    lng: Optional[float] = Query(None, description="User longitude for nearby search"),
    radius_km: Optional[float] = Query(None, description="Search radius in kilometers"),
    controller: StationController = Depends(get_station_controller)
):
    return controller.get_stations(
        city=city,
        charger_type=charger_type,
        available_only=available_only,
        lat=lat,
        lng=lng,
        radius_km=radius_km
    )

@router.get("/{station_id}", response_model=StationDetailResponse)
def get_station_by_id(
    station_id: int,
    controller: StationController = Depends(get_station_controller)
):
    return controller.get_station_by_id(station_id)

@router.post("", response_model=StationDetailResponse, status_code=status.HTTP_201_CREATED)
def create_station(
    station_in: StationCreate,
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    return admin_ctrl.create_station(
        name=station_in.name,
        city=station_in.city,
        state=station_in.state,
        country=station_in.country,
        latitude=station_in.latitude,
        longitude=station_in.longitude,
        address=station_in.address
    )

@router.put("/{station_id}", response_model=StationDetailResponse)
def update_station(
    station_id: int,
    station_in: StationUpdate,
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    return admin_ctrl.update_station(station_id, station_in.model_dump(exclude_unset=True))

@router.delete("/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(
    station_id: int,
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    admin_ctrl.delete_station(station_id)
    return None
