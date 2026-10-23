"""
APScheduler Tasks
Automated background supervisor for EVCSMS:
1. Every minute: Expire unclaimed bookings 10 minutes after start time and auto-release chargers.
2. Every minute: Send 'booking starts in 15 min' reminder notifications.
3. Every minute: Auto-release chargers whose reserved slots are vacant.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone, timedelta
from app.db.database import SessionLocal
from app.repositories.booking_repository import BookingRepository
from app.repositories.charger_repository import ChargerRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.notification_service import NotificationService

scheduler = BackgroundScheduler(daemon=True)

def monitor_and_expire_bookings():
    """
    Task 1: Expire unclaimed bookings 10 minutes past start time.
    Auto-releases the reserved charger to 'Available'.
    """
    db = SessionLocal()
    try:
        booking_repo = BookingRepository(db)
        charger_repo = ChargerRepository(db)
        notification_service = NotificationService(NotificationRepository(db))

        now = datetime.now(timezone.utc)
        threshold_time = now - timedelta(minutes=10)

        unclaimed = booking_repo.get_unclaimed_bookings(threshold_time)
        for booking in unclaimed:
            booking.status = "Expired"
            booking_repo.update(booking)

            # Auto-release charger
            charger = charger_repo.get_by_id(booking.charger_id)
            if charger and charger.status == "Reserved":
                charger_repo.update_status(charger.id, "Available")

            # Alert user
            notification_service.send_notification(
                user_id=booking.user_id,
                message=f"Booking #{booking.id} for Charger #{booking.charger_id} has expired due to 10-minute check-in timeout. Charger has been released.",
                notification_type="BOOKING_EXPIRED"
            )
            print(f"[Scheduler] Expired unclaimed booking #{booking.id} and released charger #{booking.charger_id}")
    except Exception as e:
        print(f"[Scheduler Error] monitor_and_expire_bookings failed: {e}")
    finally:
        db.close()


def send_upcoming_reminders():
    """
    Task 2: Send 'booking starts in 15 min' reminders.
    """
    db = SessionLocal()
    try:
        booking_repo = BookingRepository(db)
        notification_service = NotificationService(NotificationRepository(db))

        now = datetime.now(timezone.utc)
        window_start = now
        window_end = now + timedelta(minutes=16)

        upcoming = booking_repo.get_upcoming_bookings_for_reminder(window_start, window_end)
        for booking in upcoming:
            booking.reminder_sent = True
            booking_repo.update(booking)

            charger = booking.charger
            station_name = charger.station.name if charger and charger.station else "Charging Station"

            notification_service.send_notification(
                user_id=booking.user_id,
                message=f"Upcoming Slot Reminder: Your booking #{booking.id} at {station_name} starts within 15 minutes! Please prepare your vehicle.",
                notification_type="REMINDER_15MIN"
            )
            print(f"[Scheduler] Dispatched 15-min reminder for booking #{booking.id}")
    except Exception as e:
        print(f"[Scheduler Error] send_upcoming_reminders failed: {e}")
    finally:
        db.close()


def start_scheduler():
    """Initializes and registers periodic supervisor cron tasks."""
    if not scheduler.running:
        scheduler.add_job(
            monitor_and_expire_bookings,
            "interval",
            seconds=60,
            id="monitor_and_expire_bookings",
            replace_existing=True
        )
        scheduler.add_job(
            send_upcoming_reminders,
            "interval",
            seconds=60,
            id="send_upcoming_reminders",
            replace_existing=True
        )
        scheduler.start()
        print("[Scheduler] APScheduler background worker started successfully.")

def shutdown_scheduler():
    """Gracefully stops background supervisor."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("[Scheduler] APScheduler stopped.")
