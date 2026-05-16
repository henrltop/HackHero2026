import secrets

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from devices.models import Device, MonitoredApp
from devices.serializers import DeviceSerializer, MonitoredAppSerializer
from monitoring.serializers import TriggerSerializer


class DeviceListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        devices = Device.objects.filter(owner=request.user)
        return Response(DeviceSerializer(devices, many=True).data)

    def post(self, request):
        data = request.data.copy()
        data["device_token"] = secrets.token_hex(16)
        serializer = DeviceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MonitoredAppView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, device_token):
        device = Device.objects.get(device_token=device_token, owner=request.user)
        apps = device.monitored_apps.all()
        return Response(MonitoredAppSerializer(apps, many=True).data)

    def post(self, request, device_token):
        device = Device.objects.get(device_token=device_token, owner=request.user)
        serializer = MonitoredAppSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(device=device)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, device_token, app_id):
        device = Device.objects.get(device_token=device_token, owner=request.user)
        MonitoredApp.objects.filter(id=app_id, device=device).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeviceConfigView(APIView):
    """Usado pelo app do filho para buscar apps monitorados e gatilhos."""
    permission_classes = [AllowAny]

    def get(self, request, device_token):
        try:
            device = Device.objects.get(device_token=device_token)
        except Device.DoesNotExist:
            return Response({"detail": "Device não encontrado."}, status=404)

        apps = device.monitored_apps.filter(is_active=True).values("package_name", "app_name")
        triggers = device.triggers.all()

        return Response({
            "device_token": device_token,
            "child_name": device.child_name,
            "monitored_apps": list(apps),
            "triggers": TriggerSerializer(triggers, many=True).data,
        })
