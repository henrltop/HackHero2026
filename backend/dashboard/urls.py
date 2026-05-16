from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("",                                    views.home,          name="home"),
    path("login/",                              views.login_view,    name="login"),
    path("logout/",                             views.logout_view,   name="logout"),
    path("<str:device_token>/filters/",         views.filters_view,  name="filters"),
    path("<str:device_token>/alerts/",          views.alerts_view,   name="alerts"),
    path("api-docs/",                           views.api_docs,      name="api_docs"),
]
