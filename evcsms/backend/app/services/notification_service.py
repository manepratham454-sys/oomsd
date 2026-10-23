"""
Notification Service Layer
GRASP Principle Applied:
- High Cohesion: Focused strictly on creating, dispatching, and managing user notifications.
  Contains no charging telemetry calculations, database schema alterations, or financial logic.
"""

from typing import List, Optional
from datetime import datetime, timezone
from app.interfaces.services import INotificationService
from app.repositories.notification_repository import NotificationRepository
from app.db.models import Notification

class NotificationService(INotificationService):
    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    def send_notification(self, user_id: int, message: str, notification_type: str = "INFO") -> Notification:
        notification = Notification(
            user_id=user_id,
            message=message,
            type=notification_type,
            timestamp=datetime.now(timezone.utc),
            is_read=False
        )
        return self.notification_repo.create(notification)

    def get_user_notifications(self, user_id: int) -> List[Notification]:
        return self.notification_repo.get_user_notifications(user_id)

    def mark_as_read(self, notification_id: int, user_id: int) -> Optional[Notification]:
        return self.notification_repo.mark_as_read(notification_id, user_id)

    def mark_all_as_read(self, user_id: int) -> int:
        return self.notification_repo.mark_all_as_read(user_id)
