"""
Station and Admin Controllers
Coordinates station catalog, charger state updates, and administrative analytics.
"""

from typing import List, Dict, Any, Optional
from app.services.station_service import StationService
from app.services.report_service import ReportService
from app.db.models import Station, Charger

class StationController:
    def __init__(self, station_service: StationService):
        self.station_service = station_service

    def get_stations(
        self,
        city: Optional[str] = None,
        charger_type: Optional[str] = None,
        available_only: bool = False,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_km: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        return self.station_service.get_stations(
            city=city,
            charger_type=charger_type,
            available_only=available_only,
            lat=lat,
            lng=lng,
            radius_km=radius_km
        )

    def get_station_by_id(self, station_id: int) -> Station:
        return self.station_service.get_station_by_id(station_id)

    def get_station_chargers(self, station_id: int) -> List[Charger]:
        return self.station_service.get_station_chargers(station_id)


class AdminController:
    def __init__(self, station_service: StationService, report_service: ReportService):
        self.station_service = station_service
        self.report_service = report_service

    def create_station(self, name: str, city: str, state: str, country: str, latitude: float, longitude: float, address: Optional[str] = None) -> Station:
        return self.station_service.create_station(name, city, state, country, latitude, longitude, address)

    def update_station(self, station_id: int, updates: Dict[str, Any]) -> Station:
        return self.station_service.update_station(station_id, updates)

    def delete_station(self, station_id: int) -> None:
        self.station_service.delete_station(station_id)

    def add_charger(self, station_id: int, charger_type: str, connector_type: str, power_kw: float, price_per_unit: float, status_val: str = "Available") -> Charger:
        return self.station_service.add_charger(station_id, charger_type, connector_type, power_kw, price_per_unit, status_val)

    def update_charger_status(self, charger_id: int, status_val: str) -> Charger:
        return self.station_service.update_charger_status(charger_id, status_val)

    def update_charger_pricing(self, charger_id: int, price: float) -> Charger:
        return self.station_service.update_charger_pricing(charger_id, price)

    def delete_charger(self, charger_id: int) -> None:
        self.station_service.delete_charger(charger_id)

    def get_summary_metrics(self) -> Dict[str, Any]:
        return self.report_service.get_summary_metrics()

    def get_daily_usage(self, days: int = 7) -> List[Dict[str, Any]]:
        return self.report_service.get_daily_usage(days=days)

    def get_daily_revenue(self, days: int = 7) -> List[Dict[str, Any]]:
        return self.report_service.get_daily_revenue(days=days)

    def get_charger_utilization(self) -> List[Dict[str, Any]]:
        return self.report_service.get_charger_utilization()
