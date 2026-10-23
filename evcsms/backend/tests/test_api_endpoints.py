import pytest
from datetime import datetime, timezone

def test_auth_flow(client):
    """Test user registration, login, and /auth/me profile fetching."""
    # Register
    reg_res = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "phone_no": "+91 9999988888",
            "password": "secretpassword",
            "role": "EV_OWNER"
        }
    )
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["email"] == "janedoe@example.com"

    # Login
    login_res = client.post(
        "/api/v1/auth/login",
        json={
            "email": "janedoe@example.com",
            "password": "secretpassword"
        }
    )
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # /auth/me
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["name"] == "Jane Doe"


def test_station_search_and_filter(client, test_station_and_chargers):
    """Test station listing with city filter and geo-distance."""
    res = client.get("/api/v1/stations?city=Pune")
    assert res.status_code == 200
    stations = res.json()
    assert len(stations) >= 1
    assert stations[0]["city"] == "Pune"
    assert stations[0]["total_chargers"] == 2

    # Geo distance test near Pune (18.52, 73.85)
    geo_res = client.get("/api/v1/stations?lat=18.5200&lng=73.8500&radius_km=10")
    assert geo_res.status_code == 200
    geo_stations = geo_res.json()
    assert len(geo_stations) >= 1
    assert geo_stations[0]["distance_km"] is not None


def test_admin_reports_access_control(client, test_users):
    """Test that EV owners are forbidden (403) from accessing admin metrics while admin succeeds."""
    owner_headers = test_users["owner_headers"]
    admin_headers = test_users["admin_headers"]

    # Owner attempt -> 403 Forbidden
    res_owner = client.get("/api/v1/admin/metrics/summary", headers=owner_headers)
    assert res_owner.status_code == 403

    # Admin attempt -> 200 OK
    res_admin = client.get("/api/v1/admin/metrics/summary", headers=admin_headers)
    assert res_admin.status_code == 200
    summary = res_admin.json()
    assert "total_stations" in summary
    assert "total_chargers" in summary
