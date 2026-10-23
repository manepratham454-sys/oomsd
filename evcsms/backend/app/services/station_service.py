"""
Station & Charger Management Service
Applies Information Expert for station discovery, geo-filtering, and charger inventory.
"""

from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from app.interfaces.services import IStationService
from app.repositories.station_repository import StationRepository
from app.repositories.charger_repository import ChargerRepository
from app.db.models import Station, Charger
from app.utils.geo import calculate_haversine_distance

class StationService(IStationService):
    def __init__(self, station_repo: StationRepository, charger_repo: ChargerRepository):
        self.station_repo = station_repo
        self.charger_repo = charger_repo

    def get_stations(
        self,
        city: Optional[str] = None,
        charger_type: Optional[str] = None,
        available_only: bool = False,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_km: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        stations = self.station_repo.filter_stations(city=city)
        results = []

        for station in stations:
            chargers = station.chargers or []

            # Filter by charger type if provided (e.g. AC, DC Fast)
            if charger_type:
                chargers = [c for c in chargers if c.type.lower() == charger_type.lower()]
                if not chargers:
                    continue

            # Filter by availability if requested
            available_chargers = [c for c in chargers if c.status == "Available"]
            if available_only and not available_chargers:
                continue

            # Calculate geo distance if lat and lng provided
            dist = None
            if lat is not None and lng is not None:
                dist = calculate_haversine_distance(lat, lng, station.latitude, station.longitude)
                if radius_km is not None and dist > radius_km:
                    continue

            prices = [c.price_per_unit for c in chargers]
            min_price = min(prices) if prices else 15.0
            charger_types = list(set(c.type for c in chargers))

            results.append({
                "id": station.id,
                "name": station.name,
                "city": station.city,
                "state": station.state,
                "country": station.country,
                "latitude": station.latitude,
                "longitude": station.longitude,
                "address": station.address,
                "total_chargers": len(chargers),
                "available_chargers": len(available_chargers),
                "distance_km": dist,
                "min_price": min_price,
                "charger_types": charger_types,
            })

        # If user searched near a point, sort by distance
        if lat is not None and lng is not None:
            results.sort(key=lambda s: s["distance_km"] if s["distance_km"] is not None else 99999)

        return results

    def get_station_by_id(self, station_id: int) -> Station:
        station = self.station_repo.get_with_chargers(station_id)
        if not station:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found.")
        return station

    def create_station(self, name: str, city: str, state: str, country: str, latitude: float, longitude: float, address: Optional[str] = None) -> Station:
        station = Station(
            name=name,
            city=city,
            state=state,
            country=country,
            latitude=latitude,
            longitude=longitude,
            address=address
        )
        return self.station_repo.create(station)

    def update_station(self, station_id: int, updates: Dict[str, Any]) -> Station:
        station = self.get_station_by_id(station_id)
        for key, val in updates.items():
            if val is not None and hasattr(station, key):
                setattr(station, key, val)
        return self.station_repo.update(station)

    def delete_station(self, station_id: int) -> None:
        station = self.get_station_by_id(station_id)
        self.station_repo.delete(station)

    # Charger specific operations
    def get_station_chargers(self, station_id: int) -> List[Charger]:
        self.get_station_by_id(station_id)  # ensure station exists
        return self.charger_repo.get_by_station(station_id)

    def add_charger(self, station_id: int, charger_type: str, connector_type: str, power_kw: float, price_per_unit: float, status_val: str = "Available") -> Charger:
        self.get_station_by_id(station_id)
        charger = Charger(
            station_id=station_id,
            type=charger_type,
            connector_type=connector_type,
            power_kw=power_kw,
            price_per_unit=price_per_unit,
            status=status_val
        )
        return self.charger_repo.create(charger)

    def update_charger_status(self, charger_id: int, new_status: str) -> Charger:
        charger = self.charger_repo.get_by_id(charger_id)
        if not charger:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charger not found.")
        return self.charger_repo.update_status(charger_id, new_status)

    def update_charger_pricing(self, charger_id: int, price: float) -> Charger:
        charger = self.charger_repo.get_by_id(charger_id)
        if not charger:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charger not found.")
        return self.charger_repo.update_pricing(charger_id, price)

    def delete_charger(self, charger_id: int) -> None:
        charger = self.charger_repo.get_by_id(charger_id)
        if not charger:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charger not found.")
        self.charger_repo.delete(charger)
