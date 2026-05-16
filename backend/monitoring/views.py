from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from devices.models import Device
from monitoring.models import Alert, Trigger
from monitoring.serializers import AlertSerializer, TriggerSerializer
from services.ai_agent import analyze_image, generate_recommendations


class AnalyzeView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request):
        device_token = request.data.get("device_token")
        app_package = request.data.get("app_package", "")
        image_file = request.FILES.get("image")

        try:
            device = Device.objects.get(device_token=device_token)
        except Device.DoesNotExist:
            return Response({"detail": "Device não encontrado."}, status=404)

        image_bytes = image_file.read()
        triggers = list(device.triggers.values_list("keyword", flat=True))
        report = analyze_image(image_bytes, triggers, app_package=app_package)
        del image_bytes

        if report["risk_level"] != "safe":
            Alert.objects.create(
                device=device,
                risk_level=report["risk_level"],
                category=report["categoria"],
                description=report["descricao"],
                confidence=report["confianca"],
                app_package=app_package or None,
            )

        return Response(report)


class AlertListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        device_token = request.query_params.get("device_token")
        try:
            device = Device.objects.get(device_token=device_token, owner=request.user)
        except Device.DoesNotExist:
            return Response([])

        alerts = device.alerts.all()[:50]
        return Response(AlertSerializer(alerts, many=True).data)


class TriggerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, device_token):
        device = Device.objects.get(device_token=device_token, owner=request.user)
        return Response(TriggerSerializer(device.triggers.all(), many=True).data)

    def post(self, request, device_token):
        device = Device.objects.get(device_token=device_token, owner=request.user)
        serializer = TriggerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(device=device)
        return Response(serializer.data, status=201)

    def delete(self, request, device_token, trigger_id):
        device = Device.objects.get(device_token=device_token, owner=request.user)
        Trigger.objects.filter(id=trigger_id, device=device).delete()
        return Response(status=204)


class RecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, device_token):
        try:
            device = Device.objects.get(device_token=device_token, owner=request.user)
        except Device.DoesNotExist:
            return Response({"detail": "Device não encontrado."}, status=404)

        alerts = list(
            device.alerts.values("risk_level", "category", "description", "app_package", "created_at")[:30]
        )

        if not alerts:
            return Response({"recommendations": [
                "Nenhum alerta registrado ainda. Continue monitorando."
            ]})

        recommendations = generate_recommendations(device.child_name, alerts)
        return Response({"recommendations": recommendations})
