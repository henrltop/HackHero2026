from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    device_token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    child_name: Mapped[str] = mapped_column(String(255), nullable=False)
    fcm_token: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    owner: Mapped["User"] = relationship(back_populates="devices")
    monitored_apps: Mapped[list["MonitoredApp"]] = relationship(back_populates="device", cascade="all, delete-orphan")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="device", cascade="all, delete-orphan")
    triggers: Mapped[list["Trigger"]] = relationship(back_populates="device", cascade="all, delete-orphan")
