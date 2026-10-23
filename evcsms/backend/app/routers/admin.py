from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from app.schemas.report import DailyUsageItem, DailyRevenueItem, StationUtilizationItem, AdminDashboardSummary
from app.db.models import User
from app.controllers.station_controller import AdminController
from app.routers.deps import get_admin_controller, get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin Reports"])

@router.get("/metrics/summary", response_model=AdminDashboardSummary)
def get_metrics_summary(
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    return admin_ctrl.get_summary_metrics()

@router.get("/reports/usage", response_model=List[DailyUsageItem])
def get_usage_report(
    days: int = Query(7, ge=1, le=90, description="Reporting timeframe in days"),
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    return admin_ctrl.get_daily_usage(days=days)

@router.get("/reports/revenue", response_model=List[DailyRevenueItem])
def get_revenue_report(
    days: int = Query(7, ge=1, le=90, description="Reporting timeframe in days"),
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    return admin_ctrl.get_daily_revenue(days=days)

@router.get("/reports/utilization", response_model=List[StationUtilizationItem])
def get_utilization_report(
    current_admin: User = Depends(get_current_admin),
    admin_ctrl: AdminController = Depends(get_admin_controller)
):
    return admin_ctrl.get_charger_utilization()
