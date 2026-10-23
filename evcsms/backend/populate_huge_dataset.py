import sys
import os
import random
import uuid
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.db.models import User, Vehicle, Station, Charger, Booking, ChargingSession, Payment, Notification
from app.routers.auth import hash_password

def seed_huge_dataset():
    db = SessionLocal()
    try:
        print("--- Starting Huge Dataset Population ---")

        # 1. Ensure Default Demo Users Exist
        user = db.query(User).filter(User.email == "user@evcsms.com").first()
        if not user:
            user = User(
                name="Rahul Sharma",
                email="user@evcsms.com",
                phone_no="+91 9876543210",
                password_hash=hash_password("password123"),
                role="EV_OWNER",
                created_at=datetime.now(timezone.utc) - timedelta(days=60)
            )
            db.add(user)
            db.flush()

        admin = db.query(User).filter(User.email == "admin@evcsms.com").first()
        if not admin:
            admin = User(
                name="Priya Patel",
                email="admin@evcsms.com",
                phone_no="+91 9123456780",
                password_hash=hash_password("admin123"),
                role="ADMIN",
                created_at=datetime.now(timezone.utc) - timedelta(days=60)
            )
            db.add(admin)
            db.flush()

        # Additional EV owners for realistic multi-user density
        extra_owners_data = [
            ("Aditya Verma", "aditya.v@example.com", "+91 9822011223"),
            ("Sneha Kulkarni", "sneha.k@example.com", "+91 9822022334"),
            ("Vikram Malhotra", "vikram.m@example.com", "+91 9822033445"),
            ("Ananya Deshmukh", "ananya.d@example.com", "+91 9822044556"),
            ("Rohan Mehta", "rohan.m@example.com", "+91 9822055667"),
        ]
        owner_ids = [user.id]
        for name, email, phone in extra_owners_data:
            existing = db.query(User).filter(User.email == email).first()
            if not existing:
                u = User(
                    name=name,
                    email=email,
                    phone_no=phone,
                    password_hash=hash_password("password123"),
                    role="EV_OWNER",
                    created_at=datetime.now(timezone.utc) - timedelta(days=45)
                )
                db.add(u)
                db.flush()
                owner_ids.append(u.id)
            else:
                owner_ids.append(existing.id)

        # 2. Add Multi-vehicle Fleet for User
        user_vehicles_data = [
            ("MH 12 AB 1234", 40.5, "CCS2"),
            ("MH 14 EV 9900", 72.6, "CCS2"),
            ("MH 02 EQ 5555", 60.0, "CCS2"),
            ("MH 01 TS 3000", 24.0, "Type 2"),
        ]
        created_vehicles = []
        for reg_no, capacity, ctype in user_vehicles_data:
            v = db.query(Vehicle).filter(Vehicle.reg_no == reg_no).first()
            if not v:
                v = Vehicle(
                    reg_no=reg_no,
                    battery_capacity=capacity,
                    connector_type=ctype,
                    user_id=user.id
                )
                db.add(v)
                db.flush()
            created_vehicles.append(v)

        # 3. Comprehensive Mega Hub Network across Pune, Mumbai, Navi Mumbai, Thane, and Expressways
        stations_catalog = [
            # --- PUNE METROPOLITAN REGION (18 Stations) ---
            {
                "name": "Pune GreenCharge Hub - Hinjewadi Phase 1",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5912, "lng": 73.7389,
                "address": "Phase 1, Hinjewadi Rajiv Gandhi IT Park, near Shivaji Chowk, Pune 411057",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 22.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                    ("AC", "Type 2", 22.0, 13.0, "Available"),
                    ("AC", "Type 2", 7.4, 11.5, "Available"),
                ]
            },
            {
                "name": "Pune Quadron FastCharge - Hinjewadi Phase 2",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5975, "lng": 73.7190,
                "address": "Opposite Quadron Business Park, Phase 2, Hinjewadi, Pune 411057",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.5, "Busy"),
                    ("AC", "Type 2", 11.0, 12.5, "Available"),
                ]
            },
            {
                "name": "Pune VoltPoint Hub - Viman Nagar",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5679, "lng": 73.9143,
                "address": "Near Phoenix Marketcity, Viman Nagar, Pune 411014",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                    ("AC", "Type 2", 22.0, 13.5, "Available"),
                ]
            },
            {
                "name": "Pune EcoCharge Station - Kothrud",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5074, "lng": 73.8077,
                "address": "Paud Road, Paud Phata, Kothrud, Pune 411038",
                "chargers": [
                    ("DC Fast", "CCS2", 50.0, 17.5, "Available"),
                    ("AC", "Type 2", 7.4, 12.0, "Available"),
                ]
            },
            {
                "name": "Pune SuperCharge Hub - Baner",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5590, "lng": 73.7868,
                "address": "Baner Road, near Mumbai-Bangalore Highway, Pune 411045",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 23.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 11.0, 13.0, "Available"),
                ]
            },
            {
                "name": "Pune Metro Charge - Swargate",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5018, "lng": 73.8636,
                "address": "Swargate Multimodal Transport Hub, Pune 411042",
                "chargers": [
                    ("DC Fast", "CCS2", 50.0, 17.0, "Available"),
                    ("AC", "Type 2", 7.4, 11.5, "Available"),
                ]
            },
            {
                "name": "Pune CyberCharge - Magarpatta Cybercity",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5135, "lng": 73.9272,
                "address": "North Gate, Magarpatta City, Hadapsar, Pune 411028",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 20.5, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                    ("AC", "Type 2", 22.0, 13.0, "Available"),
                ]
            },
            {
                "name": "Pune EON FastPark - Kharadi",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5515, "lng": 73.9510,
                "address": "EON Free Zone Phase 1, Kharadi, Pune 411014",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 22.5, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                    ("AC", "Type 2", 11.0, 12.5, "Available"),
                ]
            },
            {
                "name": "Pune West AutoHub - Wakad",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5987, "lng": 73.7635,
                "address": "Dange Chowk - Wakad Flyover Link Road, Pune 411057",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                    ("AC", "Type 2", 22.0, 13.0, "Available"),
                ]
            },
            {
                "name": "Pune Heritage EV Hub - Shivajinagar",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5314, "lng": 73.8446,
                "address": "Near Shivajinagar Railway & Metro Station, Pune 411005",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                    ("AC", "Type 2", 7.4, 12.0, "Available"),
                ]
            },
            {
                "name": "Pune GreenZone - Aundh University Road",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5582, "lng": 73.8073,
                "address": "DP Road, Harmony Society, Aundh, Pune 411007",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 11.0, 12.5, "Available"),
                ]
            },
            {
                "name": "Pune Lifestyle EV Hub - Koregaon Park",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5362, "lng": 73.8940,
                "address": "North Main Road, Lane 5, Koregaon Park, Pune 411001",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.5, "Available"),
                    ("AC", "Type 2", 22.0, 14.0, "Available"),
                ]
            },
            {
                "name": "PCMC Industrial PowerHub - Pimpri",
                "city": "Pune", "state": "Maharashtra", "lat": 18.6279, "lng": 73.8009,
                "address": "Old Mumbai-Pune Highway, Pimpri Colony, Pimpri-Chinchwad 411018",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 20.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 17.5, "Available"),
                    ("AC", "Type 2", 22.0, 12.5, "Available"),
                ]
            },
            {
                "name": "PCMC Central Charge - Chinchwad",
                "city": "Pune", "state": "Maharashtra", "lat": 18.6445, "lng": 73.7912,
                "address": "Near Chinchwad Railway Station, Chinchwad, Pune 411033",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                    ("AC", "Type 2", 7.4, 11.5, "Available"),
                ]
            },
            {
                "name": "Pune South Highway Hub - Katraj",
                "city": "Pune", "state": "Maharashtra", "lat": 18.4575, "lng": 73.8677,
                "address": "Katraj Chowk, NH 48 Bypass, Katraj, Pune 411046",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 20.5, "Available"),
                    ("DC Fast", "CCS2", 50.0, 17.5, "Available"),
                ]
            },
            {
                "name": "Pune Corporate Charge - Senapati Bapat Road",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5308, "lng": 73.8290,
                "address": "ICC Trade Tower Complex, Senapati Bapat Road, Pune 411016",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 22.0, 13.5, "Available"),
                ]
            },
            {
                "name": "Pune Airport SkyCharge - Lohegaon",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5822, "lng": 73.9197,
                "address": "Pune International Airport Multilevel Car Park, Lohegaon, Pune 411032",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 23.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 22.0, 14.0, "Available"),
                ]
            },
            {
                "name": "Pune West Express - Bavdhan",
                "city": "Pune", "state": "Maharashtra", "lat": 18.5158, "lng": 73.7712,
                "address": "NDA Road, Chandani Chowk Junction, Bavdhan, Pune 411021",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.0, "Available"),
                    ("AC", "Type 2", 11.0, 12.5, "Available"),
                ]
            },

            # --- MUMBAI METROPOLITAN REGION (20 Stations) ---
            {
                "name": "Mumbai EcoPower Station - BKC G-Block",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0660, "lng": 72.8680,
                "address": "G Block, Bandra Kurla Complex, Bandra East, Mumbai 400051",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 24.0, "Available"),
                    ("DC Fast", "CCS2", 120.0, 22.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 19.5, "Available"),
                    ("AC", "Type 2", 22.0, 14.5, "Available"),
                ]
            },
            {
                "name": "Mumbai CyberCharge - Andheri East MIDC",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.1136, "lng": 72.8697,
                "address": "MIDC Central Road, Chakala, Andheri East, Mumbai 400093",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("DC Fast", "CHAdeMO", 50.0, 18.0, "Available"),
                    ("AC", "Type 2", 22.0, 14.0, "Available"),
                ]
            },
            {
                "name": "Mumbai South FastCharge - Nariman Point",
                "city": "Mumbai", "state": "Maharashtra", "lat": 18.9256, "lng": 72.8242,
                "address": "Free Press Journal Marg, Nariman Point, Mumbai 400021",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 20.0, "Available"),
                    ("AC", "Type 2", 7.4, 13.5, "Available"),
                ]
            },
            {
                "name": "Mumbai OceanView Charge - Marine Drive",
                "city": "Mumbai", "state": "Maharashtra", "lat": 18.9438, "lng": 72.8231,
                "address": "Netaji Subhash Chandra Bose Road, Churchgate, Mumbai 400020",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 20.5, "Available"),
                    ("AC", "Type 2", 22.0, 14.5, "Available"),
                ]
            },
            {
                "name": "Mumbai Business Center - Lower Parel",
                "city": "Mumbai", "state": "Maharashtra", "lat": 18.9950, "lng": 72.8300,
                "address": "Senapati Bapat Marg, Lower Parel, Mumbai 400013",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 24.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 20.0, "Available"),
                    ("AC", "Type 2", 22.0, 14.0, "Available"),
                ]
            },
            {
                "name": "Mumbai Tech Hub - Powai Hiranandani",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.1176, "lng": 72.9060,
                "address": "Central Avenue, Hiranandani Gardens, Powai, Mumbai 400076",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 22.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 22.0, 13.5, "Available"),
                ]
            },
            {
                "name": "Mumbai Coastal SuperHub - Worli Sea Face",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0178, "lng": 72.8154,
                "address": "Dr Annie Besant Road, Worli, Mumbai 400018",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 22.0, "Available"),
                    ("AC", "Type 2", 22.0, 14.0, "Available"),
                ]
            },
            {
                "name": "Mumbai Heritage Port - Dadar Shivaji Park",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0269, "lng": 72.8378,
                "address": "Cadell Road, Shivaji Park, Dadar West, Mumbai 400028",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 7.4, 12.5, "Available"),
                ]
            },
            {
                "name": "Mumbai Western Express - Andheri West Lokhandwala",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.1432, "lng": 72.8267,
                "address": "Lokhandwala Complex, Andheri West, Mumbai 400053",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.5, "Available"),
                    ("AC", "Type 2", 22.0, 14.0, "Available"),
                ]
            },
            {
                "name": "Mumbai Queen's Suburb - Bandra West",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0596, "lng": 72.8295,
                "address": "Linking Road, Bandra West, Mumbai 400050",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 20.0, "Available"),
                    ("AC", "Type 2", 11.0, 13.5, "Available"),
                ]
            },
            {
                "name": "Mumbai North Express - Borivali National Park",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.2288, "lng": 72.8598,
                "address": "Western Express Highway, near SGNP Gate, Borivali East, Mumbai 400066",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 22.0, 13.0, "Available"),
                ]
            },
            {
                "name": "Mumbai Corporate Port - Malad Mindspace",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.1764, "lng": 72.8361,
                "address": "Link Road, Mindspace, Malad West, Mumbai 400064",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.5, "Available"),
                    ("AC", "Type 2", 22.0, 13.5, "Available"),
                ]
            },
            {
                "name": "Mumbai Highway Hub - Goregaon Nesco",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.1558, "lng": 72.8530,
                "address": "Western Express Highway, Goregaon East, Mumbai 400063",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 23.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                ]
            },
            {
                "name": "Mumbai Seaside Hub - Juhu Tara Road",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0988, "lng": 72.8267,
                "address": "Juhu Tara Road, near Juhu Beach, Mumbai 400049",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 20.0, "Available"),
                    ("AC", "Type 2", 7.4, 13.0, "Available"),
                ]
            },
            {
                "name": "Mumbai Eastern Suburbs - Chembur Diamond Garden",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0522, "lng": 72.8994,
                "address": "Sion-Trombay Road, Chembur, Mumbai 400071",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 11.0, 12.5, "Available"),
                ]
            },
            {
                "name": "Mumbai Retail Hub - Kurla Phoenix Marketcity",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0860, "lng": 72.8890,
                "address": "LBS Marg, Kurla West, Mumbai 400070",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 22.0, 13.5, "Available"),
                ]
            },
            {
                "name": "Mumbai Central Connect - Ghatkopar R-City",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0998, "lng": 72.9163,
                "address": "LBS Marg, Amrut Nagar, Ghatkopar West, Mumbai 400086",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 22.0, 13.0, "Available"),
                ]
            },
            {
                "name": "CSMIA International Terminal T2 EV Hub",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0974, "lng": 72.8744,
                "address": "Chhatrapati Shivaji Maharaj International Airport T2, Sahar, Mumbai 400099",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 25.0, "Available"),
                    ("DC Fast", "CCS2", 120.0, 22.5, "Available"),
                    ("AC", "Type 2", 22.0, 15.0, "Available"),
                ]
            },
            {
                "name": "Mumbai South Harbour - Colaba Cuffe Parade",
                "city": "Mumbai", "state": "Maharashtra", "lat": 18.9130, "lng": 72.8210,
                "address": "Captain Prakash Pethe Marg, Cuffe Parade, Mumbai 400005",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 20.0, "Available"),
                    ("AC", "Type 2", 7.4, 13.5, "Available"),
                ]
            },
            {
                "name": "Mumbai Transit Hub - Sion Circle",
                "city": "Mumbai", "state": "Maharashtra", "lat": 19.0390, "lng": 72.8619,
                "address": "Dr Ambedkar Road, Sion Circle, Mumbai 400022",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 11.0, 12.5, "Available"),
                ]
            },

            # --- NAVI MUMBAI (8 Stations) ---
            {
                "name": "Navi Mumbai MegaCharger - Vashi Sector 17",
                "city": "Navi Mumbai", "state": "Maharashtra", "lat": 19.0771, "lng": 72.9986,
                "address": "Sector 17, near Palm Beach Road, Vashi, Navi Mumbai 400703",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.0, "Available"),
                    ("DC Fast", "CCS2", 50.0, 17.5, "Available"),
                    ("AC", "Type 2", 22.0, 13.0, "Available"),
                ]
            },
            {
                "name": "Navi Mumbai Central - Belapur CBD",
                "city": "Navi Mumbai", "state": "Maharashtra", "lat": 19.0180, "lng": 73.0400,
                "address": "Sector 11, CBD Belapur, Navi Mumbai 400614",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 20.5, "Available"),
                    ("AC", "Type 2", 22.0, 13.0, "Available"),
                ]
            },
            {
                "name": "Navi Mumbai Greens - Kharghar Central Park",
                "city": "Navi Mumbai", "state": "Maharashtra", "lat": 19.0434, "lng": 73.0683,
                "address": "Sector 23, near Central Park, Kharghar, Navi Mumbai 410210",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 11.0, 12.5, "Available"),
                ]
            },
            {
                "name": "Navi Mumbai Grand Mall - Seawoods",
                "city": "Navi Mumbai", "state": "Maharashtra", "lat": 19.0205, "lng": 73.0185,
                "address": "Seawoods Grand Central Mall, Sector 40, Nerul, Navi Mumbai 400706",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 22.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 22.0, 13.5, "Available"),
                ]
            },
            {
                "name": "Navi Mumbai Gateway - Panvel Highway Hub",
                "city": "Navi Mumbai", "state": "Maharashtra", "lat": 18.9894, "lng": 73.1175,
                "address": "Old Mumbai-Pune Highway, Panvel, Navi Mumbai 410206",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 22.5, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                ]
            },
            {
                "name": "Navi Mumbai TechPark - Airoli Mindspace",
                "city": "Navi Mumbai", "state": "Maharashtra", "lat": 19.1578, "lng": 72.9980,
                "address": "Mindspace SEZ, Airoli West, Navi Mumbai 400708",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.0, "Available"),
                    ("AC", "Type 2", 22.0, 13.0, "Available"),
                ]
            },
            {
                "name": "Navi Mumbai Industrial - Ghansoli RCP",
                "city": "Navi Mumbai", "state": "Maharashtra", "lat": 19.1245, "lng": 73.0089,
                "address": "Thane-Belapur Road, Ghansoli, Navi Mumbai 400701",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 7.4, 12.0, "Available"),
                ]
            },
            {
                "name": "Navi Mumbai Coast - Nerul Palm Beach",
                "city": "Navi Mumbai", "state": "Maharashtra", "lat": 19.0345, "lng": 73.0189,
                "address": "Palm Beach Road, Sector 20, Nerul, Navi Mumbai 400706",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 11.0, 13.0, "Available"),
                ]
            },

            # --- THANE (8 Stations) ---
            {
                "name": "Thane Express EV Hub - Viviana Majiwada",
                "city": "Thane", "state": "Maharashtra", "lat": 19.2183, "lng": 72.9781,
                "address": "Near Viviana Mall, Eastern Express Highway, Thane 400606",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 22.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 22.0, 13.0, "Available"),
                ]
            },
            {
                "name": "Thane North Link - Ghodbunder Road",
                "city": "Thane", "state": "Maharashtra", "lat": 19.2625, "lng": 72.9644,
                "address": "Ghodbunder Road, near Suraj Water Park, Waghbil, Thane 400615",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                ]
            },
            {
                "name": "Thane Premium Hub - Hiranandani Estate",
                "city": "Thane", "state": "Maharashtra", "lat": 19.2550, "lng": 72.9850,
                "address": "The Walk, Hiranandani Estate, Ghodbunder Road, Thane 400607",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.5, "Available"),
                    ("AC", "Type 2", 22.0, 14.0, "Available"),
                ]
            },
            {
                "name": "Thane Industrial Hub - Wagle Estate",
                "city": "Thane", "state": "Maharashtra", "lat": 19.1930, "lng": 72.9520,
                "address": "Road No 16, Wagle Industrial Estate, Thane West 400604",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                    ("AC", "Type 2", 7.4, 12.0, "Available"),
                ]
            },
            {
                "name": "Thane City Center - Naupada",
                "city": "Thane", "state": "Maharashtra", "lat": 19.1868, "lng": 72.9715,
                "address": "Gokhale Road, near Talao Pali, Naupada, Thane West 400602",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.5, "Available"),
                    ("AC", "Type 2", 11.0, 12.5, "Available"),
                ]
            },
            {
                "name": "Thane Suburban - Kasarvadavali",
                "city": "Thane", "state": "Maharashtra", "lat": 19.2780, "lng": 72.9720,
                "address": "Near Hypercity Mall, Kasarvadavali, Ghodbunder Road, Thane 400615",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 18.0, "Available"),
                    ("AC", "Type 2", 7.4, 12.0, "Available"),
                ]
            },
            {
                "name": "Thane Rail Transit Hub - Thane Station",
                "city": "Thane", "state": "Maharashtra", "lat": 19.1860, "lng": 72.9758,
                "address": "Station Road, Thane West, Thane 400601",
                "chargers": [
                    ("DC Fast", "CCS2", 50.0, 17.5, "Available"),
                    ("AC", "Type 2", 7.4, 11.5, "Available"),
                ]
            },
            {
                "name": "Thane Green Zone - Yeoor Hills Gate",
                "city": "Thane", "state": "Maharashtra", "lat": 19.2150, "lng": 72.9420,
                "address": "Upvan Lake Road, near Yeoor Gate, Thane West 400606",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 11.0, 13.0, "Available"),
                ]
            },

            # --- MUMBAI-PUNE EXPRESSWAY & GHATS HIGHWAY CORRIDOR (6 Stations) ---
            {
                "name": "Expressway MegaHub - Khalapur Food Mall",
                "city": "Expressway", "state": "Maharashtra", "lat": 18.8350, "lng": 73.2850,
                "address": "Km 42, Mumbai-Pune Expressway Food Plaza, Khalapur, Raigad 410203",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 24.0, "Available"),
                    ("DC Fast", "CCS2", 150.0, 24.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 20.0, "Available"),
                    ("AC", "Type 2", 22.0, 15.0, "Available"),
                ]
            },
            {
                "name": "Expressway FastPark - Talegaon Urse Toll",
                "city": "Expressway", "state": "Maharashtra", "lat": 18.7250, "lng": 73.6550,
                "address": "Urse Toll Plaza Rest Area, Mumbai-Pune Expressway, Talegaon 410506",
                "chargers": [
                    ("DC Fast", "CCS2", 150.0, 23.5, "Available"),
                    ("DC Fast", "CCS2", 60.0, 19.5, "Available"),
                    ("AC", "Type 2", 22.0, 14.0, "Available"),
                ]
            },
            {
                "name": "Lonavala Hill Station EV Hub - Wax Museum",
                "city": "Lonavala", "state": "Maharashtra", "lat": 18.7557, "lng": 73.4091,
                "address": "Old Mumbai-Pune Highway, Varsoli, Lonavala 410401",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 22.0, "Available"),
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 11.0, 13.5, "Available"),
                ]
            },
            {
                "name": "Khandala Ghat Scenic Charge - Amrutanjan Point",
                "city": "Lonavala", "state": "Maharashtra", "lat": 18.7620, "lng": 73.3750,
                "address": "Near Duke's Nose Viewpoint, Khandala Ghat, Lonavala 410301",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.5, "Available"),
                    ("AC", "Type 2", 7.4, 13.0, "Available"),
                ]
            },
            {
                "name": "Khopoli Valley EV Station - Toll Bypass",
                "city": "Khopoli", "state": "Maharashtra", "lat": 18.7890, "lng": 73.3420,
                "address": "Khopoli Bypass Junction, SH 104, Khopoli 410203",
                "chargers": [
                    ("DC Fast", "CCS2", 60.0, 19.0, "Available"),
                    ("AC", "Type 2", 11.0, 13.0, "Available"),
                ]
            },
            {
                "name": "Expressway Midway Oasis - Somatane Phata",
                "city": "Expressway", "state": "Maharashtra", "lat": 18.7050, "lng": 73.6920,
                "address": "Somatane Toll Interchange, NH 48, Maval, Pune 410506",
                "chargers": [
                    ("DC Fast", "CCS2", 120.0, 21.0, "Available"),
                    ("AC", "Type 2", 22.0, 13.5, "Available"),
                ]
            },
        ]

        # 4. Insert or Update Stations and Chargers
        total_chargers_count = 0
        all_chargers = []
        for sdata in stations_catalog:
            station = db.query(Station).filter(Station.name == sdata["name"]).first()
            if not station:
                station = Station(
                    name=sdata["name"],
                    city=sdata["city"],
                    state=sdata["state"],
                    country="India",
                    latitude=sdata["lat"],
                    longitude=sdata["lng"],
                    address=sdata["address"],
                    created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(15, 60))
                )
                db.add(station)
                db.flush()

            # Chargers
            for c_type, connector, power, price, status in sdata["chargers"]:
                ch = db.query(Charger).filter(
                    Charger.station_id == station.id,
                    Charger.power_kw == power,
                    Charger.connector_type == connector
                ).first()
                if not ch:
                    ch = Charger(
                        station_id=station.id,
                        type=c_type,
                        connector_type=connector,
                        power_kw=power,
                        price_per_unit=price,
                        status=status
                    )
                    db.add(ch)
                    db.flush()
                all_chargers.append(ch)
                total_chargers_count += 1

        db.commit()
        print(f"Loaded {len(stations_catalog)} Charging Hubs and {total_chargers_count} Chargers into database!")

        # 5. Populate Historical & Recent Bookings, Charging Sessions & Payments
        # Generate 40 past completed bookings with sessions and payments
        now = datetime.now(timezone.utc)
        completed_bookings_count = 0

        for i in range(1, 41):
            past_days = random.randint(1, 30)
            past_hour = random.randint(8, 20)
            start_dt = (now - timedelta(days=past_days)).replace(hour=past_hour, minute=0, second=0, microsecond=0)
            duration_minutes = random.choice([30, 45, 60, 90])
            end_dt = start_dt + timedelta(minutes=duration_minutes)

            assigned_user_id = random.choice(owner_ids)
            assigned_vehicle = random.choice(created_vehicles) if assigned_user_id == user.id else None
            assigned_charger = random.choice(all_chargers)

            # Check if booking exists
            b = Booking(
                user_id=assigned_user_id,
                charger_id=assigned_charger.id,
                vehicle_id=assigned_vehicle.id if assigned_vehicle else None,
                start_time=start_dt,
                end_time=end_dt,
                status="Completed",
                reminder_sent=True,
                created_at=start_dt - timedelta(hours=2)
            )
            db.add(b)
            db.flush()

            # Create Completed Session
            units = round(random.uniform(18.0, 58.0), 2)
            cost = round(units * assigned_charger.price_per_unit, 2)
            sess = ChargingSession(
                booking_id=b.id,
                start_time=start_dt,
                end_time=end_dt,
                units_consumed=units,
                total_cost=cost,
                status="Completed"
            )
            db.add(sess)
            db.flush()

            # Create Payment
            pm = Payment(
                session_id=sess.id,
                amount=cost,
                payment_mode=random.choice(["UPI", "Card", "Wallet"]),
                status="Success",
                transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
                created_at=end_dt + timedelta(minutes=2)
            )
            db.add(pm)
            completed_bookings_count += 1

        # 6. Create 3 Upcoming Confirmed Bookings for user@evcsms.com
        for day_offset, hour in [(1, 10), (2, 14), (4, 18)]:
            future_start = (now + timedelta(days=day_offset)).replace(hour=hour, minute=0, second=0, microsecond=0)
            future_end = future_start + timedelta(minutes=60)
            future_charger = random.choice(all_chargers)

            fb = Booking(
                user_id=user.id,
                charger_id=future_charger.id,
                vehicle_id=created_vehicles[0].id,
                start_time=future_start,
                end_time=future_end,
                status="Confirmed",
                reminder_sent=False,
                created_at=now - timedelta(hours=1)
            )
            db.add(fb)

        # 7. Add Realistic Notifications
        notif_samples = [
            ("Booking Confirmed: Hinjewadi Phase 1 DC Fast 150kW slot reserved for tomorrow.", "BOOKING_CONFIRMED"),
            ("Charging Session Completed: 42.5 kWh delivered. Total: ₹935.00 paid via UPI.", "PAYMENT_SUCCESS"),
            ("Reminder: Your charging slot at BKC G-Block starts in 15 minutes.", "REMINDER_15MIN"),
            ("EVCSMS Corridor Alert: 12 new Ultra-Fast 150kW hubs activated along Mumbai-Pune Expressway.", "INFO"),
        ]
        for msg, ntype in notif_samples:
            n = Notification(
                user_id=user.id,
                message=msg,
                type=ntype,
                is_read=False,
                timestamp=now - timedelta(hours=random.randint(1, 24))
            )
            db.add(n)

        db.commit()
        print(f"Added {completed_bookings_count} historical sessions and 3 upcoming bookings.")
        print("--- Huge Dataset Seeded Successfully! ---")

    except Exception as e:
        db.rollback()
        print(f"Error seeding huge dataset: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_huge_dataset()
