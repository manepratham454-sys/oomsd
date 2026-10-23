"""
Seed Script for EV Charging Station Management System (EVCSMS)
Populates:
- 1 Station Admin: admin@evcsms.com / adminpassword123
- 1 EV Owner: owner@evcsms.com / ownerpassword123 with registered vehicles
- 2 Stations: Pune (Hinjewadi) and Mumbai (BKC)
- 6 Chargers: AC and DC Fast chargers with different connector types (CCS2, Type 2, CHAdeMO)
- Sample historical session, payment, and analytics data
"""

import sys
import os
from datetime import datetime, timezone, timedelta

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine, SessionLocal, Base
from app.db.models import User, Vehicle, Station, Charger, Booking, ChargingSession, Payment, Admin, Notification
from app.utils.security import hash_password

def seed_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        admin_user = db.query(User).filter(User.email == "admin@evcsms.com").first()
        if admin_user:
            print("Database already contains seed data. Skipping re-seeding.")
            return

        print("Seeding Admin User...")
        admin_user = User(
            name="Priya Deshmukh (Station Admin)",
            email="admin@evcsms.com",
            phone_no="+91 9820011223",
            password_hash=hash_password("adminpassword123"),
            role="ADMIN",
            created_at=datetime.now(timezone.utc)
        )
        db.add(admin_user)
        db.flush()

        admin_profile = Admin(
            user_id=admin_user.id,
            name=admin_user.name,
            email=admin_user.email
        )
        db.add(admin_profile)

        print("Seeding EV Owner...")
        ev_owner = User(
            name="Rahul Sharma",
            email="owner@evcsms.com",
            phone_no="+91 9876543210",
            password_hash=hash_password("ownerpassword123"),
            role="EV_OWNER",
            created_at=datetime.now(timezone.utc)
        )
        db.add(ev_owner)
        db.flush()

        print("Seeding EV Owner's Vehicles...")
        v1 = Vehicle(
            reg_no="MH-12-EV-2024",
            battery_capacity=40.5,  # Tata Nexon EV
            connector_type="CCS2",
            user_id=ev_owner.id
        )
        v2 = Vehicle(
            reg_no="MH-01-EV-9999",
            battery_capacity=72.6,  # Hyundai Ioniq 5
            connector_type="CCS2",
            user_id=ev_owner.id
        )
        db.add_all([v1, v2])
        db.flush()

        print("Seeding Stations (Pune & Mumbai)...")
        pune_station = Station(
            name="Pune GreenCharge Hub - Hinjewadi",
            city="Pune",
            state="Maharashtra",
            country="India",
            latitude=18.5913,
            longitude=73.7389,
            address="Phase 1, Hinjewadi IT Park, near Shivaji Chowk, Pune, Maharashtra 411057",
            created_at=datetime.now(timezone.utc) - timedelta(days=10)
        )

        mumbai_station = Station(
            name="Mumbai EcoPower Station - BKC",
            city="Mumbai",
            state="Maharashtra",
            country="India",
            latitude=19.0657,
            longitude=72.8687,
            address="G Block, Bandra Kurla Complex, Bandra East, Mumbai, Maharashtra 400051",
            created_at=datetime.now(timezone.utc) - timedelta(days=10)
        )
        db.add_all([pune_station, mumbai_station])
        db.flush()

        print("Seeding 6 Chargers...")
        chargers = [
            # Pune Chargers
            Charger(
                station_id=pune_station.id,
                type="DC Fast",
                connector_type="CCS2",
                power_kw=60.0,
                price_per_unit=18.50,
                status="Available"
            ),
            Charger(
                station_id=pune_station.id,
                type="DC Fast",
                connector_type="CCS2",
                power_kw=50.0,
                price_per_unit=17.00,
                status="Available"
            ),
            Charger(
                station_id=pune_station.id,
                type="AC",
                connector_type="Type 2",
                power_kw=7.4,
                price_per_unit=12.00,
                status="Available"
            ),
            # Mumbai Chargers
            Charger(
                station_id=mumbai_station.id,
                type="DC Fast",
                connector_type="CCS2",
                power_kw=120.0,
                price_per_unit=22.00,
                status="Available"
            ),
            Charger(
                station_id=mumbai_station.id,
                type="DC Fast",
                connector_type="CHAdeMO",
                power_kw=50.0,
                price_per_unit=18.00,
                status="Available"
            ),
            Charger(
                station_id=mumbai_station.id,
                type="AC",
                connector_type="Type 2",
                power_kw=22.0,
                price_per_unit=14.00,
                status="Available"
            ),
        ]
        db.add_all(chargers)
        db.flush()

        print("Seeding Sample Completed History & Notifications for Analytics...")
        now = datetime.now(timezone.utc)
        # Historical booking 1 day ago
        past_booking = Booking(
            user_id=ev_owner.id,
            charger_id=chargers[0].id,
            vehicle_id=v1.id,
            start_time=now - timedelta(days=1, hours=2),
            end_time=now - timedelta(days=1, hours=1),
            status="Completed",
            reminder_sent=True,
            created_at=now - timedelta(days=1, hours=3)
        )
        db.add(past_booking)
        db.flush()

        past_session = ChargingSession(
            booking_id=past_booking.id,
            start_time=now - timedelta(days=1, hours=2),
            end_time=now - timedelta(days=1, hours=1),
            units_consumed=28.5,  # 28.5 kWh
            total_cost=round(28.5 * 18.50, 2),  # 527.25 INR
            status="Completed"
        )
        db.add(past_session)
        db.flush()

        past_payment = Payment(
            session_id=past_session.id,
            amount=past_session.total_cost,
            payment_mode="UPI",
            status="Success",
            transaction_id="UPI-DEMO789012",
            created_at=now - timedelta(days=1, hours=1)
        )
        db.add(past_payment)

        # Another past session in Mumbai 2 days ago for rich analytics
        past_booking_2 = Booking(
            user_id=ev_owner.id,
            charger_id=chargers[3].id,
            vehicle_id=v2.id,
            start_time=now - timedelta(days=2, hours=4),
            end_time=now - timedelta(days=2, hours=3),
            status="Completed",
            reminder_sent=True,
            created_at=now - timedelta(days=2, hours=5)
        )
        db.add(past_booking_2)
        db.flush()

        past_session_2 = ChargingSession(
            booking_id=past_booking_2.id,
            start_time=now - timedelta(days=2, hours=4),
            end_time=now - timedelta(days=2, hours=3),
            units_consumed=45.0,
            total_cost=round(45.0 * 22.00, 2),  # 990.00 INR
            status="Completed"
        )
        db.add(past_session_2)
        db.flush()

        past_payment_2 = Payment(
            session_id=past_session_2.id,
            amount=past_session_2.total_cost,
            payment_mode="Card",
            status="Success",
            transaction_id="CARD-DEMO334455",
            created_at=now - timedelta(days=2, hours=3)
        )
        db.add(past_payment_2)

        # Seed welcome notifications
        notif1 = Notification(
            user_id=ev_owner.id,
            message="Welcome to EVCSMS! Your account is active and vehicle MH-12-EV-2024 is registered.",
            timestamp=now - timedelta(days=3),
            type="INFO",
            is_read=True
        )
        notif2 = Notification(
            user_id=ev_owner.id,
            message="Payment of ₹527.25 for charging session at Pune GreenCharge Hub was successful.",
            timestamp=now - timedelta(days=1, hours=1),
            type="PAYMENT_SUCCESS",
            is_read=False
        )
        db.add_all([notif1, notif2])

        db.commit()
        print("Successfully seeded EVCSMS database!")
        print("  Admin Account: admin@evcsms.com / adminpassword123")
        print("  EV Owner Account: owner@evcsms.com / ownerpassword123")
        print(f"  Stations: {pune_station.name}, {mumbai_station.name}")
        print(f"  Total Chargers: {len(chargers)}")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

    # Also seed the full network of additional stations
    try:
        from add_all_stations import add_stations
        add_stations()
    except Exception as e:
        print(f"Note: Extended station seeding skipped: {e}")

if __name__ == "__main__":
    seed_database()
