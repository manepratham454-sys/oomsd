import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.db.models import User, Vehicle, Station, Charger
from app.utils.security import hash_password, create_access_token

# In-memory SQLite engine for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Creates a fresh in-memory database for each test function."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_users(db_session):
    """Create test EV Owner and Admin users."""
    owner = User(
        name="Test Owner",
        email="testowner@example.com",
        password_hash=hash_password("password123"),
        role="EV_OWNER",
        created_at=datetime.now(timezone.utc)
    )
    admin = User(
        name="Test Admin",
        email="testadmin@example.com",
        password_hash=hash_password("password123"),
        role="ADMIN",
        created_at=datetime.now(timezone.utc)
    )
    db_session.add_all([owner, admin])
    db_session.commit()
    db_session.refresh(owner)
    db_session.refresh(admin)

    # Add a vehicle for owner
    vehicle = Vehicle(
        reg_no="DL-01-EV-1234",
        battery_capacity=50.0,
        connector_type="CCS2",
        user_id=owner.id
    )
    db_session.add(vehicle)
    db_session.commit()
    db_session.refresh(vehicle)

    owner_token = create_access_token({"sub": owner.email, "role": owner.role, "user_id": owner.id})
    admin_token = create_access_token({"sub": admin.email, "role": admin.role, "user_id": admin.id})

    return {
        "owner": owner,
        "admin": admin,
        "vehicle": vehicle,
        "owner_headers": {"Authorization": f"Bearer {owner_token}"},
        "admin_headers": {"Authorization": f"Bearer {admin_token}"},
    }

@pytest.fixture
def test_station_and_chargers(db_session):
    """Create test station with AC and DC Fast chargers."""
    station = Station(
        name="Test Metro Station",
        city="Pune",
        state="Maharashtra",
        country="India",
        latitude=18.5204,
        longitude=73.8567,
        address="FC Road, Pune",
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(station)
    db_session.commit()
    db_session.refresh(station)

    charger1 = Charger(
        station_id=station.id,
        type="DC Fast",
        connector_type="CCS2",
        power_kw=60.0,
        price_per_unit=18.0,
        status="Available"
    )
    charger2 = Charger(
        station_id=station.id,
        type="AC",
        connector_type="Type 2",
        power_kw=7.4,
        price_per_unit=12.0,
        status="Available"
    )
    db_session.add_all([charger1, charger2])
    db_session.commit()
    db_session.refresh(charger1)
    db_session.refresh(charger2)

    return {
        "station": station,
        "charger1": charger1,
        "charger2": charger2
    }
