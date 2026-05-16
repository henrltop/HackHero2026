from datetime import datetime
from pydantic import BaseModel


class AlertOut(BaseModel):
    id: int
    device_id: int
    risk_level: str
    category: str
    description: str
    confidence: float
    app_package: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
