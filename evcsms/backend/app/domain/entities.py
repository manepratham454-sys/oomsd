"""
Domain Entities Layer
Demonstrating Object-Oriented Software Modeling and Design (OOSMD) principles:
- GRASP Patterns (Information Expert, Creator, Low Coupling, High Cohesion, Controller)
- SOLID Principles (Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion)
"""

from datetime import datetime, timezone
from typing import Optional, List
import uuid

def current_time():
    return datetime.now(timezone.utc)


class Vehicle:
    """
    Domain Entity: Vehicle
    OOSMD Principle: High Cohesion - Encapsulates EV battery specifications and connector type.
    """
    def __init__(self, vehicle_id: Optional[int], reg_no: str, battery_capacity: float, connector_type: str, user_id: int):
        self.vehicle_id = vehicle_id
        self.reg_no = reg_no
        self.battery_capacity = battery_capacity
        self.connector_type = connector_type
        self.user_id = user_id

    def is_compatible_with(self, charger_connector: str) -> bool:
        """Check if vehicle can connect to the target charger port."""
        return self.connector_type.strip().lower() == charger_connector.strip().lower()


class Charger:
    """
    Domain Entity: Charger
    OOSMD Principle: Information Expert - Owns its current operational state, power rating, and tariff.
    """
    STATUS_AVAILABLE = "Available"
    STATUS_BUSY = "Busy"
    STATUS_RESERVED = "Reserved"
    STATUS_OFFLINE = "Offline"

    def __init__(self, charger_id: Optional[int], station_id: int, charger_type: str, connector_type: str,
                 power_kw: float, status: str = "Available", price_per_unit: float = 15.0):
        self.charger_id = charger_id
        self.station_id = station_id
        self.charger_type = charger_type  # AC, DC Fast
        self.connector_type = connector_type  # CCS2, Type 2, CHAdeMO
        self.power_kw = power_kw
        self.status = status
        self.price_per_unit = price_per_unit

    def reserve(self):
        if self.status != self.STATUS_AVAILABLE:
            raise ValueError(f"Charger {self.charger_id} cannot be reserved because it is currently {self.status}.")
        self.status = self.STATUS_RESERVED

    def start_charging(self):
        self.status = self.STATUS_BUSY

    def release(self):
        self.status = self.STATUS_AVAILABLE


class ChargingStation:
    """
    Domain Entity: ChargingStation
    OOSMD Principle: High Cohesion - Aggregates physical location details and associated chargers.
    """
    def __init__(self, station_id: Optional[int], name: str, city: str, state: str, country: str,
                 latitude: float, longitude: float, address: Optional[str] = None):
        self.station_id = station_id
        self.name = name
        self.city = city
        self.state = state
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.chargers: List[Charger] = []

    def add_charger(self, charger: Charger):
        self.chargers.append(charger)


class ChargingSession:
    """
    Domain Entity: ChargingSession
    OOSMD Principle: GRASP Information Expert -
    The ChargingSession maintains energy meter telemetry and duration,
    and is therefore the Information Expert responsible for calculating units consumed and total billing cost.
    """
    def __init__(self, session_id: Optional[int], booking_id: int, start_time: datetime,
                 end_time: Optional[datetime] = None, units_consumed: float = 0.0,
                 total_cost: float = 0.0, status: str = "Active"):
        self.session_id = session_id
        self.booking_id = booking_id
        self.start_time = start_time
        self.end_time = end_time
        self.units_consumed = units_consumed
        self.total_cost = total_cost
        self.status = status

    def compute_energy_and_cost(self, charger_power_kw: float, price_per_unit: float, end_time: Optional[datetime] = None) -> float:
        """
        Information Expert calculation:
        Energy (kWh) = Power (kW) * Duration (hours)
        Cost (INR) = Energy (kWh) * PricePerUnit (INR/kWh)
        """
        self.end_time = end_time or current_time()
        # Calculate duration in hours
        duration_seconds = max((self.end_time - self.start_time).total_seconds(), 0)
        duration_hours = duration_seconds / 3600.0

        # Compute consumed energy units
        self.units_consumed = round(charger_power_kw * duration_hours, 2)
        # Minimum billable threshold for simulation realism: 0.1 kWh if session executed
        if duration_seconds > 1 and self.units_consumed == 0.0:
            self.units_consumed = 0.1

        self.total_cost = round(self.units_consumed * price_per_unit, 2)
        self.status = "Completed"
        return self.total_cost


class Booking:
    """
    Domain Entity: Booking
    OOSMD Principle: GRASP Creator -
    The Booking holds the reservation window and links the User with the Charger.
    It has the necessary initialization context to create the ChargingSession when the vehicle plugs in.
    """
    STATUS_CONFIRMED = "Confirmed"
    STATUS_PENDING = "Pending"
    STATUS_CANCELLED = "Cancelled"
    STATUS_COMPLETED = "Completed"
    STATUS_EXPIRED = "Expired"

    def __init__(self, booking_id: Optional[int], user_id: int, charger_id: int,
                 start_time: datetime, end_time: datetime, vehicle_id: Optional[int] = None,
                 status: str = "Confirmed", reminder_sent: bool = False):
        self.booking_id = booking_id
        self.user_id = user_id
        self.charger_id = charger_id
        self.vehicle_id = vehicle_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.reminder_sent = reminder_sent

    def create_session(self) -> ChargingSession:
        """
        GRASP Creator Pattern: Booking creates ChargingSession instances.
        Ensures valid booking status before instantiation.
        """
        if self.status != self.STATUS_CONFIRMED:
            raise ValueError(f"Cannot initiate charging session: Booking #{self.booking_id} is in status '{self.status}'.")

        return ChargingSession(
            session_id=None,
            booking_id=self.booking_id if self.booking_id else 0,
            start_time=current_time(),
            units_consumed=0.0,
            total_cost=0.0,
            status="Active"
        )

    def cancel(self):
        if self.status in [self.STATUS_COMPLETED, self.STATUS_EXPIRED]:
            raise ValueError(f"Cannot cancel a booking that is already {self.status}.")
        self.status = self.STATUS_CANCELLED

    def expire(self):
        self.status = self.STATUS_EXPIRED


class Payment:
    """
    Domain Entity: Payment
    OOSMD Principle: GRASP Low Coupling -
    Depends only on ChargingSession and User; does not hold tight dependencies
    on hardware chargers, routing, or database layers.
    """
    def __init__(self, payment_id: Optional[int], session_id: int, amount: float,
                 payment_mode: str, status: str = "Pending", transaction_id: Optional[str] = None):
        self.payment_id = payment_id
        self.session_id = session_id
        self.amount = amount
        self.payment_mode = payment_mode
        self.status = status
        self.transaction_id = transaction_id or f"TXN-{uuid.uuid4().hex[:10].upper()}"


class Notification:
    """
    Domain Entity: Notification
    OOSMD Principle: GRASP High Cohesion -
    Only handles alerting messages, timestamps, and receipt state.
    Contains no station management or payment processing logic.
    """
    def __init__(self, notification_id: Optional[int], user_id: int, message: str,
                 notification_type: str = "INFO", timestamp: Optional[datetime] = None, is_read: bool = False):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.notification_type = notification_type
        self.timestamp = timestamp or current_time()
        self.is_read = is_read

    def mark_as_read(self):
        self.is_read = True


class EVOwner:
    """
    Domain Entity: EVOwner (Actor)
    OOSMD Principle: Single Responsibility Principle (SRP) -
    Represents the consumer in the EV ecosystem managing personal vehicles and bookings.
    """
    def __init__(self, user_id: Optional[int], name: str, email: str, phone_no: Optional[str] = None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone_no = phone_no
        self.role = "EV_OWNER"
        self.vehicles: List[Vehicle] = []


class Admin:
    """
    Domain Entity: Admin (Actor)
    OOSMD Principle: Single Responsibility Principle (SRP) -
    Represents the station operator managing infrastructure, pricing, and analytics.
    """
    def __init__(self, admin_id: Optional[int], user_id: int, name: str, email: str):
        self.admin_id = admin_id
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = "ADMIN"
