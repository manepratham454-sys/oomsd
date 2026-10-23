import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.db.models import Station, Charger

def add_stations():
    db = SessionLocal()
    try:
        new_stations_data = [
            {
                "name": "Pune VoltPoint Hub - Viman Nagar",
                "city": "Pune",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 18.5679,
                "longitude": 73.9143,
                "address": "Near Phoenix Marketcity, Viman Nagar, Pune, Maharashtra 411014",
                "chargers": [
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 120.0, "price_per_unit": 21.0, "status": "Available"},
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 60.0, "price_per_unit": 18.0, "status": "Available"},
                    {"type": "AC", "connector_type": "Type 2", "power_kw": 22.0, "price_per_unit": 13.5, "status": "Available"},
                ]
            },
            {
                "name": "Pune EcoCharge Station - Kothrud",
                "city": "Pune",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 18.5074,
                "longitude": 73.8077,
                "address": "Paud Road, Paud Phata, Kothrud, Pune, Maharashtra 411038",
                "chargers": [
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 50.0, "price_per_unit": 17.5, "status": "Available"},
                    {"type": "AC", "connector_type": "Type 2", "power_kw": 7.4, "price_per_unit": 12.0, "status": "Available"},
                ]
            },
            {
                "name": "Pune SuperCharge Hub - Baner",
                "city": "Pune",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 18.5590,
                "longitude": 73.7868,
                "address": "Baner Road, near Expressway Junction, Pune, Maharashtra 411045",
                "chargers": [
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 150.0, "price_per_unit": 23.0, "status": "Available"},
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 60.0, "price_per_unit": 18.5, "status": "Available"},
                    {"type": "AC", "connector_type": "Type 2", "power_kw": 11.0, "price_per_unit": 13.0, "status": "Available"},
                ]
            },
            {
                "name": "Pune Metro Charge - Swargate",
                "city": "Pune",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 18.5018,
                "longitude": 73.8636,
                "address": "Swargate Transport Terminal Hub, Pune, Maharashtra 411042",
                "chargers": [
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 50.0, "price_per_unit": 17.0, "status": "Available"},
                    {"type": "AC", "connector_type": "Type 2", "power_kw": 7.4, "price_per_unit": 11.5, "status": "Available"},
                ]
            },
            {
                "name": "Mumbai CyberCharge - Andheri East",
                "city": "Mumbai",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 19.1136,
                "longitude": 72.8697,
                "address": "MIDC Central Road, Chakala, Andheri East, Mumbai, Maharashtra 400093",
                "chargers": [
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 60.0, "price_per_unit": 19.0, "status": "Available"},
                    {"type": "DC Fast", "connector_type": "CHAdeMO", "power_kw": 50.0, "price_per_unit": 18.0, "status": "Available"},
                    {"type": "AC", "connector_type": "Type 2", "power_kw": 22.0, "price_per_unit": 14.0, "status": "Available"},
                ]
            },
            {
                "name": "Mumbai South FastCharge - Nariman Point",
                "city": "Mumbai",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 18.9256,
                "longitude": 72.8242,
                "address": "Free Press Journal Marg, Nariman Point, Mumbai, Maharashtra 400021",
                "chargers": [
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 60.0, "price_per_unit": 20.0, "status": "Available"},
                    {"type": "AC", "connector_type": "Type 2", "power_kw": 7.4, "price_per_unit": 13.5, "status": "Available"},
                ]
            },
            {
                "name": "Navi Mumbai MegaCharger - Vashi",
                "city": "Navi Mumbai",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 19.0771,
                "longitude": 72.9986,
                "address": "Sector 17, near Palm Beach Road, Vashi, Navi Mumbai, Maharashtra 400703",
                "chargers": [
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 120.0, "price_per_unit": 21.0, "status": "Available"},
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 50.0, "price_per_unit": 17.5, "status": "Available"},
                    {"type": "AC", "connector_type": "Type 2", "power_kw": 22.0, "price_per_unit": 13.0, "status": "Available"},
                ]
            },
            {
                "name": "Thane Express EV Hub - Majiwada",
                "city": "Thane",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 19.2183,
                "longitude": 72.9781,
                "address": "Near Viviana Mall, Eastern Express Highway, Thane, Maharashtra 400606",
                "chargers": [
                    {"type": "DC Fast", "connector_type": "CCS2", "power_kw": 60.0, "price_per_unit": 18.5, "status": "Available"},
                    {"type": "AC", "connector_type": "Type 2", "power_kw": 7.4, "price_per_unit": 12.5, "status": "Available"},
                ]
            }
        ]

        added_count = 0
        for data in new_stations_data:
            existing = db.query(Station).filter(Station.name == data["name"]).first()
            if existing:
                continue

            station = Station(
                name=data["name"],
                city=data["city"],
                state=data["state"],
                country=data["country"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                address=data["address"],
                created_at=datetime.now(timezone.utc) - timedelta(days=5)
            )
            db.add(station)
            db.flush()

            for c in data["chargers"]:
                charger = Charger(
                    station_id=station.id,
                    type=c["type"],
                    connector_type=c["connector_type"],
                    power_kw=c["power_kw"],
                    price_per_unit=c["price_per_unit"],
                    status=c["status"]
                )
                db.add(charger)

            added_count += 1

        db.commit()
        print(f"Added {added_count} new charging stations successfully!")
        all_stations = db.query(Station).all()
        print(f"Total stations in network: {len(all_stations)}")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_stations()
