"""
Interface Segregation Principle (ISP) & Dependency Inversion Principle (DIP):
Clients should not be forced to depend on methods they do not use.
IBookingService, IPaymentService, IStationService, ISessionService, and INotificationService
are distinct, focused interfaces defining high-level contracts.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

class IBookingService(ABC):
    """
    Interface Segregation Principle (ISP):
    Defines strictly booking-related capabilities without polluting with payment or hardware control.
    """
    @abstractmethod
    def create_booking(self, user_id: int, charger_id: int, start_time: datetime, end_time: datetime, vehicle_id: Optional[int] = None) -> Any:
        pass

    @abstractmethod
    def get_user_bookings(self, user_id: int) -> List[Any]:
        pass

    @abstractmethod
    def cancel_booking(self, booking_id: int, user_id: int) -> Any:
        pass

    @abstractmethod
    def check_slot_conflict(self, charger_id: int, start_time: datetime, end_time: datetime, exclude_booking_id: Optional[int] = None) -> bool:
        pass


class IPaymentService(ABC):
    """
    Interface Segregation Principle (ISP) & Single Responsibility Principle (SRP):
    Dedicated solely to financial transaction processing and invoice generation.
    """
    @abstractmethod
    def process_payment(self, session_id: int, user_id: int, payment_mode: str, details: Optional[Dict[str, Any]] = None) -> Any:
        pass

    @abstractmethod
    def get_user_payments(self, user_id: int) -> List[Any]:
        pass

    @abstractmethod
    def get_invoice(self, payment_id: int, user_id: int, is_admin: bool = False) -> Any:
        pass


class IStationService(ABC):
    """
    Interface Segregation Principle (ISP):
    Station discovery, filtering, geolocation search, and charger telemetry querying.
    """
    @abstractmethod
    def get_stations(self, city: Optional[str] = None, charger_type: Optional[str] = None,
                     available_only: bool = False, lat: Optional[float] = None,
                     lng: Optional[float] = None, radius_km: float = 50.0) -> List[Any]:
        pass

    @abstractmethod
    def get_station_by_id(self, station_id: int) -> Any:
        pass


class ISessionService(ABC):
    """
    Interface Segregation Principle (ISP):
    Coordinates charging hardware sessions and metering calculations.
    """
    @abstractmethod
    def start_session(self, booking_id: int, user_id: int) -> Any:
        pass

    @abstractmethod
    def stop_session(self, session_id: int, user_id: int, custom_units: Optional[float] = None) -> Any:
        pass

    @abstractmethod
    def get_session(self, session_id: int) -> Any:
        pass


class INotificationService(ABC):
    """
    Interface Segregation Principle (ISP) & High Cohesion:
    Notification dispatching and unread state management.
    """
    @abstractmethod
    def send_notification(self, user_id: int, message: str, notification_type: str = "INFO") -> Any:
        pass

    @abstractmethod
    def get_user_notifications(self, user_id: int) -> List[Any]:
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: int, user_id: int) -> Any:
        pass
