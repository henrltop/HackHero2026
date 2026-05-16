from django.urls import path
from monitoring.views import AlertListView, AnalyzeView, TriggerView

urlpatterns = [
    path("analyze/", AnalyzeView.as_view()),
    path("alerts/", AlertListView.as_view()),
    path("devices/<str:device_token>/triggers/", TriggerView.as_view()),
    path("devices/<str:device_token>/triggers/<int:trigger_id>/", TriggerView.as_view()),
]
