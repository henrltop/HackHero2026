from django.contrib import admin
from devices.models import Device, MonitoredApp


class MonitoredAppInline(admin.TabularInline):
    model = MonitoredApp
    extra = 0


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["child_name", "owner", "device_token", "created_at"]
    inlines = [MonitoredAppInline]


@admin.register(MonitoredApp)
class MonitoredAppAdmin(admin.ModelAdmin):
    list_display = ["app_name", "package_name", "device", "is_active"]
    list_filter = ["is_active"]
