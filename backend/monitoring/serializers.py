from rest_framework import serializers
from monitoring.models import Trigger, Alert


class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        fields = ["id", "keyword", "category"]


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["id", "device_id", "risk_level", "category", "description", "confidence", "app_package", "created_at"]
