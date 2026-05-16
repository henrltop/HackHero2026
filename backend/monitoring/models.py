from django.db import models


class Trigger(models.Model):
    device = models.ForeignKey("devices.Device", on_delete=models.CASCADE, related_name="triggers")
    keyword = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.keyword} ({self.category})"


class Alert(models.Model):
    RISK_LEVELS = [
        ("safe", "Seguro"),
        ("attention", "Atenção"),
        ("high_risk", "Alto Risco"),
    ]
    device = models.ForeignKey("devices.Device", on_delete=models.CASCADE, related_name="alerts")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    confidence = models.FloatField(default=0.0)
    app_package = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_risk_level_display()} — {self.device} — {self.created_at:%d/%m %H:%M}"
