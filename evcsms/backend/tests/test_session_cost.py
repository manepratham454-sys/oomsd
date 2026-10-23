import pytest
from datetime import datetime, timezone, timedelta
from app.domain.entities import ChargingSession, Booking as DomainBooking

def test_domain_session_cost_calculation():
    """
    Test GRASP Information Expert:
    ChargingSession calculates energy units and total cost based on duration, power kW, and price per unit.
    """
    start_time = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    end_time = datetime(2026, 1, 1, 11, 30, 0, tzinfo=timezone.utc)  # 1.5 hours duration

    session = ChargingSession(
        session_id=1,
        booking_id=101,
        start_time=start_time,
        status="Active"
    )

    power_kw = 50.0  # 50 kW charger
    price_per_unit = 20.0  # ₹20 / kWh

    total_cost = session.compute_energy_and_cost(
        charger_power_kw=power_kw,
        price_per_unit=price_per_unit,
        end_time=end_time
    )

    # 50 kW * 1.5 h = 75 kWh
    assert session.units_consumed == 75.0
    # 75 kWh * 20 ₹/kWh = 1500.00 ₹
    assert session.total_cost == 1500.0
    assert total_cost == 1500.0
    assert session.status == "Completed"


def test_session_lifecycle_and_cost_api(client, test_users, test_station_and_chargers):
    """
    Test full session flow via API:
    1. Create a booking starting now
    2. Start charging session
    3. Stop charging session with specified energy units
    4. Validate cost calculation
    """
    headers = test_users["owner_headers"]
    charger = test_station_and_chargers["charger1"]
    vehicle = test_users["vehicle"]

    now = datetime.now(timezone.utc)
    booking_res = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "charger_id": charger.id,
            "vehicle_id": vehicle.id,
            "start_time": (now - timedelta(minutes=5)).isoformat(),
            "end_time": (now + timedelta(hours=1)).isoformat()
        }
    )
    assert booking_res.status_code == 201
    booking_id = booking_res.json()["id"]

    # Start session
    start_res = client.post(
        "/api/v1/sessions/start",
        headers=headers,
        json={"booking_id": booking_id}
    )
    assert start_res.status_code == 201
    session_id = start_res.json()["id"]
    assert start_res.json()["status"] == "Active"

    # Stop session with 30 kWh
    stop_res = client.post(
        f"/api/v1/sessions/{session_id}/stop",
        headers=headers,
        json={"custom_units": 30.0}
    )
    assert stop_res.status_code == 200
    data = stop_res.json()
    assert data["status"] == "Completed"
    assert data["units_consumed"] == 30.0
    # Price is 18.0 * 30.0 = 540.0
    assert data["total_cost"] == 540.0
