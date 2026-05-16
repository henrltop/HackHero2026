from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.device import Device
from app.models.alert import Alert
from app.schemas.analyze import RiskReport
from app.services.ai_agent import analyze_image

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.post("", response_model=RiskReport)
async def analyze(
    image: UploadFile = File(...),
    device_token: str = Form(...),
    app_package: str = Form(default=""),
    db: Session = Depends(get_db),
):
    device = db.query(Device).filter(Device.device_token == device_token).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device não encontrado")

    image_bytes = await image.read()

    triggers = [t.keyword for t in device.triggers]
    report = await analyze_image(image_bytes, triggers)

    del image_bytes

    if report.risk_level != "safe":
        alert = Alert(
            device_id=device.id,
            risk_level=report.risk_level,
            category=report.detected_triggers[0] if report.detected_triggers else "geral",
            description=report.description,
            confidence=report.confidence,
            app_package=app_package or None,
        )
        db.add(alert)
        db.commit()

    return report
