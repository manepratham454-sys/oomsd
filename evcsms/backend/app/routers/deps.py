"""
FastAPI Dependencies & Dependency Inversion Principle (DIP)
All layers (Repositories -> Services -> Controllers) are wired and injected here.
Enables clean test swapping with mock repositories and services.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.utils.security import decode_access_token
from app.db.models import User

# Repositories
from app.repositories.user_repository import UserRepository, VehicleRepository
from app.repositories.station_repository import StationRepository, ChargerRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.payment_repository import PaymentRepository, NotificationRepository

# Services
from app.services.notification_service import NotificationService
from app.services.station_service import StationService
from app.services.booking_service import BookingService
from app.services.session_service import SessionService
from app.services.payment.payment_service import PaymentService
from app.services.report_service import ReportService

# Controllers
from app.controllers.booking_controller import BookingController
from app.controllers.session_controller import SessionController
from app.controllers.payment_controller import PaymentController
from app.controllers.station_controller import StationController, AdminController

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# --- Repository Dependencies ---
def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_vehicle_repo(db: Session = Depends(get_db)) -> VehicleRepository:
    return VehicleRepository(db)

def get_station_repo(db: Session = Depends(get_db)) -> StationRepository:
    return StationRepository(db)

def get_charger_repo(db: Session = Depends(get_db)) -> ChargerRepository:
    return ChargerRepository(db)

def get_booking_repo(db: Session = Depends(get_db)) -> BookingRepository:
    return BookingRepository(db)

def get_session_repo(db: Session = Depends(get_db)) -> SessionRepository:
    return SessionRepository(db)

def get_payment_repo(db: Session = Depends(get_db)) -> PaymentRepository:
    return PaymentRepository(db)

def get_notification_repo(db: Session = Depends(get_db)) -> NotificationRepository:
    return NotificationRepository(db)

# --- Service Dependencies ---
def get_notification_service(repo: NotificationRepository = Depends(get_notification_repo)) -> NotificationService:
    return NotificationService(repo)

def get_station_service(
    station_repo: StationRepository = Depends(get_station_repo),
    charger_repo: ChargerRepository = Depends(get_charger_repo)
) -> StationService:
    return StationService(station_repo, charger_repo)

def get_booking_service(
    booking_repo: BookingRepository = Depends(get_booking_repo),
    charger_repo: ChargerRepository = Depends(get_charger_repo),
    vehicle_repo: VehicleRepository = Depends(get_vehicle_repo),
    notification_service: NotificationService = Depends(get_notification_service),
) -> BookingService:
    return BookingService(booking_repo, charger_repo, vehicle_repo, notification_service)

def get_session_service(
    session_repo: SessionRepository = Depends(get_session_repo),
    booking_repo: BookingRepository = Depends(get_booking_repo),
    charger_repo: ChargerRepository = Depends(get_charger_repo),
    notification_service: NotificationService = Depends(get_notification_service),
) -> SessionService:
    return SessionService(session_repo, booking_repo, charger_repo, notification_service)

def get_payment_service(
    payment_repo: PaymentRepository = Depends(get_payment_repo),
    session_repo: SessionRepository = Depends(get_session_repo),
) -> PaymentService:
    return PaymentService(payment_repo, session_repo)

def get_report_service(db: Session = Depends(get_db)) -> ReportService:
    return ReportService(db)

# --- Controller Dependencies ---
def get_booking_controller(service: BookingService = Depends(get_booking_service)) -> BookingController:
    return BookingController(service)

def get_session_controller(service: SessionService = Depends(get_session_service)) -> SessionController:
    return SessionController(service)

def get_payment_controller(service: PaymentService = Depends(get_payment_service)) -> PaymentController:
    return PaymentController(service)

def get_station_controller(service: StationService = Depends(get_station_service)) -> StationController:
    return StationController(service)

def get_admin_controller(
    station_service: StationService = Depends(get_station_service),
    report_service: ReportService = Depends(get_report_service),
) -> AdminController:
    return AdminController(station_service, report_service)

# --- Authentication Dependencies ---
def get_current_user(token: str = Depends(oauth2_scheme), user_repo: UserRepository = Depends(get_user_repo)) -> User:
    payload = decode_access_token(token)
    email: str = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject.")
    user = user_repo.get_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
    return user

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required.")
    return current_user
