from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from app.db.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone_no = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="EV_OWNER", nullable=False)  # EV_OWNER, ADMIN
    created_at = Column(DateTime, default=utcnow)

    # Relationships
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    admin_profile = relationship("Admin", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    reg_no = Column(String(50), unique=True, index=True, nullable=False)
    battery_capacity = Column(Float, nullable=False)  # in kWh (e.g. 40.5, 75.0)
    connector_type = Column(String(50), nullable=False)  # CCS2, Type 2, CHAdeMO, GB/T
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="vehicles")
    bookings = relationship("Booking", back_populates="vehicle")


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    country = Column(String(100), default="India", nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=utcnow)

    chargers = relationship("Charger", back_populates="station", cascade="all, delete-orphan")


class Charger(Base):
    __tablename__ = "chargers"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    type = Column(String(50), nullable=False)  # AC, DC Fast
    connector_type = Column(String(50), default="CCS2", nullable=False)  # CCS2, Type 2, CHAdeMO
    power_kw = Column(Float, default=50.0, nullable=False)  # kW rating (e.g. 7.4, 22.0, 50.0, 60.0)
    status = Column(String(50), default="Available", nullable=False)  # Available, Busy, Reserved, Offline
    price_per_unit = Column(Float, default=15.0, nullable=False)  # Price in INR per kWh

    station = relationship("Station", back_populates="chargers")
    bookings = relationship("Booking", back_populates="charger", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    charger_id = Column(Integer, ForeignKey("chargers.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="Confirmed", nullable=False)  # Pending, Confirmed, Cancelled, Completed, Expired
    reminder_sent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utcnow)

    user = relationship("User", back_populates="bookings")
    charger = relationship("Charger", back_populates="bookings")
    vehicle = relationship("Vehicle", back_populates="bookings")
    session = relationship("ChargingSession", back_populates="booking", uselist=False, cascade="all, delete-orphan")


class ChargingSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, unique=True)
    start_time = Column(DateTime, default=utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    units_consumed = Column(Float, default=0.0, nullable=False)  # kWh
    total_cost = Column(Float, default=0.0, nullable=False)  # INR
    status = Column(String(50), default="Active", nullable=False)  # Active, Completed

    booking = relationship("Booking", back_populates="session")
    payment = relationship("Payment", back_populates="session", uselist=False, cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, unique=True)
    amount = Column(Float, nullable=False)
    payment_mode = Column(String(50), nullable=False)  # UPI, Card, Wallet
    status = Column(String(50), default="Pending", nullable=False)  # Pending, Success, Failed
    transaction_id = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=utcnow)

    session = relationship("ChargingSession", back_populates="payment")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)

    user = relationship("User", back_populates="admin_profile")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=utcnow, nullable=False)
    type = Column(String(50), default="INFO", nullable=False)  # BOOKING_CONFIRMED, REMINDER_15MIN, BOOKING_EXPIRED, SESSION_STARTED, SESSION_COMPLETED, PAYMENT_SUCCESS
    is_read = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="notifications")
