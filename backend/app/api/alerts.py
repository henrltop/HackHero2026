from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.alert import Alert
from app.models.device import Device
from app.schemas.alert import AlertOut

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertOut])
def list_alerts(
    device_token: str = Query(...),
    limit: int = Query(default=50, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    device = (
        db.query(Device)
        .filter(Device.device_token == device_token, Device.owner_id == current_user.id)
        .first()
    )
    if not device:
        return []

    return (
        db.query(Alert)
        .filter(Alert.device_id == device.id)
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .all()
    )
