"""
Admin Reporting and Analytics Service
Generates aggregations for usage, revenue, and charger utilization metrics.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from app.db.models import Station, Charger, Booking, ChargingSession, Payment, User

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_summary_metrics(self) -> Dict[str, Any]:
        total_stations = self.db.query(func.count(Station.id)).scalar() or 0
        total_chargers = self.db.query(func.count(Charger.id)).scalar() or 0
        active_sessions = self.db.query(func.count(ChargingSession.id)).filter(ChargingSession.status == "Active").scalar() or 0
        total_revenue = self.db.query(func.sum(Payment.amount)).filter(Payment.status == "Success").scalar() or 0.0
        total_energy = self.db.query(func.sum(ChargingSession.units_consumed)).scalar() or 0.0
        total_users = self.db.query(func.count(User.id)).filter(User.role == "EV_OWNER").scalar() or 0

        return {
            "total_stations": total_stations,
            "total_chargers": total_chargers,
            "active_sessions": active_sessions,
            "total_revenue_overall": round(float(total_revenue), 2),
            "total_energy_delivered_kwh": round(float(total_energy), 2),
            "total_users": total_users,
        }

    def get_daily_usage(self, days: int = 7) -> List[Dict[str, Any]]:
        """Usage aggregated per station per day for the last N days."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        sessions = (
            self.db.query(
                func.date(ChargingSession.start_time).label("session_date"),
                Station.id.label("station_id"),
                Station.name.label("station_name"),
                func.count(ChargingSession.id).label("total_sessions"),
                func.sum(ChargingSession.units_consumed).label("total_energy_kwh")
            )
            .join(Booking, ChargingSession.booking_id == Booking.id)
            .join(Charger, Booking.charger_id == Charger.id)
            .join(Station, Charger.station_id == Station.id)
            .filter(ChargingSession.start_time >= cutoff)
            .group_by(func.date(ChargingSession.start_time), Station.id, Station.name)
            .order_by(func.date(ChargingSession.start_time).asc())
            .all()
        )

        results = []
        for row in sessions:
            results.append({
                "date": str(row.session_date),
                "station_id": row.station_id,
                "station_name": row.station_name,
                "total_sessions": row.total_sessions,
                "total_energy_kwh": round(float(row.total_energy_kwh or 0), 2),
            })
        return results

    def get_daily_revenue(self, days: int = 7) -> List[Dict[str, Any]]:
        """Revenue aggregated per station per day."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        payments = (
            self.db.query(
                func.date(Payment.created_at).label("payment_date"),
                Station.id.label("station_id"),
                Station.name.label("station_name"),
                func.sum(Payment.amount).label("total_revenue"),
                func.count(Payment.id).label("total_payments")
            )
            .join(ChargingSession, Payment.session_id == ChargingSession.id)
            .join(Booking, ChargingSession.booking_id == Booking.id)
            .join(Charger, Booking.charger_id == Charger.id)
            .join(Station, Charger.station_id == Station.id)
            .filter(Payment.created_at >= cutoff, Payment.status == "Success")
            .group_by(func.date(Payment.created_at), Station.id, Station.name)
            .order_by(func.date(Payment.created_at).asc())
            .all()
        )

        results = []
        for row in payments:
            results.append({
                "date": str(row.payment_date),
                "station_id": row.station_id,
                "station_name": row.station_name,
                "total_revenue": round(float(row.total_revenue or 0), 2),
                "total_payments": row.total_payments,
            })
        return results

    def get_charger_utilization(self) -> List[Dict[str, Any]]:
        """Current utilization rates per station."""
        stations = self.db.query(Station).all()
        results = []

        for st in stations:
            chargers = st.chargers or []
            total = len(chargers)
            busy = sum(1 for c in chargers if c.status == "Busy")
            reserved = sum(1 for c in chargers if c.status == "Reserved")
            available = sum(1 for c in chargers if c.status == "Available")
            rate = round(((busy + reserved) / total * 100), 1) if total > 0 else 0.0

            results.append({
                "station_id": st.id,
                "station_name": st.name,
                "city": st.city,
                "total_chargers": total,
                "busy_chargers": busy,
                "reserved_chargers": reserved,
                "available_chargers": available,
                "utilization_rate_pct": rate,
            })
        return results
