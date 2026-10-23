import pytest
from datetime import datetime, timezone, timedelta
from app.db.models import Booking

def test_booking_slot_conflict(client, test_users, test_station_and_chargers):
    """
    Test that overlapping booking slots for the same charger are strictly rejected (409 Conflict).
    """
    headers = test_users["owner_headers"]
    charger_id = test_station_and_chargers["charger1"].id
    vehicle_id = test_users["vehicle"].id

    base_time = datetime.now(timezone.utc) + timedelta(days=1)
    slot1_start = (base_time.replace(hour=10, minute=0, second=0, microsecond=0)).isoformat()
    slot1_end = (base_time.replace(hour=11, minute=0, second=0, microsecond=0)).isoformat()

    # 1. Create first booking: 10:00 - 11:00
    res1 = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "charger_id": charger_id,
            "vehicle_id": vehicle_id,
            "start_time": slot1_start,
            "end_time": slot1_end
        }
    )
    assert res1.status_code == 201, f"Failed to create first booking: {res1.text}"
    booking1 = res1.json()
    assert booking1["status"] == "Confirmed"

    # 2. Attempt overlapping booking: 10:30 - 11:30 (overlaps with 10:00 - 11:00)
    slot2_start = (base_time.replace(hour=10, minute=30, second=0, microsecond=0)).isoformat()
    slot2_end = (base_time.replace(hour=11, minute=30, second=0, microsecond=0)).isoformat()

    res2 = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "charger_id": charger_id,
            "vehicle_id": vehicle_id,
            "start_time": slot2_start,
            "end_time": slot2_end
        }
    )
    assert res2.status_code == 409, "Overlapping booking was not rejected!"
    assert "conflicts with an existing booking" in res2.json()["detail"]

    # 3. Attempt non-overlapping booking: 11:00 - 12:00 (adjacent/after) should succeed
    slot3_start = (base_time.replace(hour=11, minute=0, second=0, microsecond=0)).isoformat()
    slot3_end = (base_time.replace(hour=12, minute=0, second=0, microsecond=0)).isoformat()

    res3 = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "charger_id": charger_id,
            "vehicle_id": vehicle_id,
            "start_time": slot3_start,
            "end_time": slot3_end
        }
    )
    assert res3.status_code == 201, f"Non-overlapping booking failed: {res3.text}"


def test_vehicle_connector_compatibility(client, test_users, test_station_and_chargers):
    """
    Test that booking validates connector compatibility with the selected vehicle:
    Vehicle has connector 'CCS2'.
    Charger 1 has 'CCS2' -> Compatible (201 Created).
    Charger 2 has 'Type 2' -> Incompatible (400 Bad Request).
    """
    headers = test_users["owner_headers"]
    charger1_id = test_station_and_chargers["charger1"].id  # CCS2
    charger2_id = test_station_and_chargers["charger2"].id  # Type 2
    vehicle_id = test_users["vehicle"].id  # CCS2

    base_time = datetime.now(timezone.utc) + timedelta(days=2)
    start_time = (base_time.replace(hour=14, minute=0, second=0, microsecond=0)).isoformat()
    end_time = (base_time.replace(hour=15, minute=0, second=0, microsecond=0)).isoformat()

    # Attempt booking Charger 2 (Type 2) with vehicle (CCS2)
    res_incompatible = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "charger_id": charger2_id,
            "vehicle_id": vehicle_id,
            "start_time": start_time,
            "end_time": end_time
        }
    )
    assert res_incompatible.status_code == 400
    assert "Connector mismatch" in res_incompatible.json()["detail"]

    # Now book Charger 1 (CCS2) with vehicle (CCS2)
    res_compatible = client.post(
        "/api/v1/bookings",
        headers=headers,
        json={
            "charger_id": charger1_id,
            "vehicle_id": vehicle_id,
            "start_time": start_time,
            "end_time": end_time
        }
    )
    assert res_compatible.status_code == 201
