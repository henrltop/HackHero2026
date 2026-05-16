from django.contrib import admin
from monitoring.models import Alert, Trigger


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ["created_at", "device", "risk_level", "category", "confidence", "app_package"]
    list_filter = ["risk_level", "category"]
    search_fields = ["description", "device__child_name"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ["keyword", "category", "device"]
    list_filter = ["category"]
