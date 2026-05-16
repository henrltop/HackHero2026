from pydantic import BaseModel


class RiskReport(BaseModel):
    risk_level: str  # safe | attention | high_risk
    confidence: float
    detected_triggers: list[str]
    description: str
