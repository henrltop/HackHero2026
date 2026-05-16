from rest_framework import serializers
from devices.models import Device, MonitoredApp


class MonitoredAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoredApp
        fields = ["id", "package_name", "app_name", "is_active"]


class DeviceSerializer(serializers.ModelSerializer):
    monitored_apps = MonitoredAppSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ["id", "device_token", "child_name", "fcm_token", "created_at", "monitored_apps"]
        read_only_fields = ["device_token", "created_at"]
