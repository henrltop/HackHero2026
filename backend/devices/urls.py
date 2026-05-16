from django.urls import path
from devices.views import DeviceListCreateView, MonitoredAppView, DeviceConfigView

urlpatterns = [
    path("devices/", DeviceListCreateView.as_view()),
    path("devices/<str:device_token>/apps/", MonitoredAppView.as_view()),
    path("devices/<str:device_token>/apps/<int:app_id>/", MonitoredAppView.as_view()),
    path("devices/<str:device_token>/config/", DeviceConfigView.as_view()),
]
