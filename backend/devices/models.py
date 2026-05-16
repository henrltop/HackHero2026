from django.conf import settings
from django.db import models


class Device(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="devices")
    device_token = models.CharField(max_length=64, unique=True, db_index=True)
    child_name = models.CharField(max_length=255)
    fcm_token = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.child_name} ({self.device_token[:8]}…)"


class MonitoredApp(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="monitored_apps")
    package_name = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.app_name} — {self.device}"
