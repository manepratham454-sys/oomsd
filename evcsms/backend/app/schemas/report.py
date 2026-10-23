from pydantic import BaseModel
from typing import List, Optional

class DailyUsageItem(BaseModel):
    date: str
    station_id: int
    station_name: str
    total_sessions: int
    total_energy_kwh: float

class DailyRevenueItem(BaseModel):
    date: str
    station_id: int
    station_name: str
    total_revenue: float
    total_payments: int

class StationUtilizationItem(BaseModel):
    station_id: int
    station_name: str
    city: str
    total_chargers: int
    busy_chargers: int
    reserved_chargers: int
    available_chargers: int
    utilization_rate_pct: float

class AdminDashboardSummary(BaseModel):
    total_stations: int
    total_chargers: int
    active_sessions: int
    total_revenue_overall: float
    total_energy_delivered_kwh: float
    total_users: int
