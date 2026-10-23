from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.db.models import User, Vehicle
from app.repositories.user_repository import VehicleRepository
from app.routers.deps import get_vehicle_repo, get_current_user

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.get("/my", response_model=List[VehicleResponse])
def get_my_vehicles(
    current_user: User = Depends(get_current_user),
    vehicle_repo: VehicleRepository = Depends(get_vehicle_repo)
):
    return vehicle_repo.get_by_user_id(current_user.id)

@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def add_vehicle(
    vehicle_in: VehicleCreate,
    current_user: User = Depends(get_current_user),
    vehicle_repo: VehicleRepository = Depends(get_vehicle_repo)
):
    existing = vehicle_repo.get_by_reg_no(vehicle_in.reg_no.strip())
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A vehicle with this registration number is already registered.")

    vehicle = Vehicle(
        reg_no=vehicle_in.reg_no.strip().upper(),
        battery_capacity=vehicle_in.battery_capacity,
        connector_type=vehicle_in.connector_type.strip(),
        user_id=current_user.id
    )
    return vehicle_repo.create(vehicle)

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int,
    current_user: User = Depends(get_current_user),
    vehicle_repo: VehicleRepository = Depends(get_vehicle_repo)
):
    vehicle = vehicle_repo.get_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")
    if vehicle.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this vehicle.")
    vehicle_repo.delete(vehicle)
    return None
