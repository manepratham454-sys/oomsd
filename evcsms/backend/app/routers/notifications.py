from fastapi import APIRouter, Depends
from typing import List
from app.schemas.notification import NotificationResponse, NotificationReadResponse
from app.db.models import User
from app.services.notification_service import NotificationService
from app.routers.deps import get_notification_service, get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[NotificationResponse])
def get_my_notifications(
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
):
    return service.get_user_notifications(current_user.id)

@router.patch("/{notification_id}/read", response_model=NotificationReadResponse)
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
):
    notif = service.mark_as_read(notification_id, current_user.id)
    return {"id": notification_id, "is_read": True if notif else False}

@router.patch("/read-all", response_model=dict)
def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
):
    count = service.mark_all_as_read(current_user.id)
    return {"status": "success", "marked_read_count": count}
