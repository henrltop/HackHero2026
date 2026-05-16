from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from devices.models import Device, MonitoredApp
from monitoring.models import Alert, Trigger
from services.ai_agent import get_risk_info

RISK_THEMES = [
    ("financial",    "Informações Financeiras",  "Dados bancários, faturas e orçamentos",         "💰"),
    ("personal_data","Dados Pessoais (LGPD)",     "CPF, endereços e registros sensíveis",          "🪪"),
    ("corporate",    "Segredos Corporativos",     "Patentes, códigos e planos industriais",        "🔒"),
    ("adult",        "Conteúdo Adulto",           "Imagens ou textos impróprios para a idade",     "🔞"),
    ("harassment",   "Assédio e Hostilidade",     "Linguagem ofensiva e comportamentos tóxicos",  "⚠️"),
    ("malware",      "Infiltração de Malware",    "Links suspeitos e arquivos perigosos",          "🛡️"),
]


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    error = None
    if request.method == "POST":
        user = authenticate(request, username=request.POST["email"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect("dashboard:home")
        error = "E-mail ou senha incorretos."
    return render(request, "dashboard/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("dashboard:login")


@login_required
def home(request):
    devices = Device.objects.filter(owner=request.user).prefetch_related("alerts")
    return render(request, "dashboard/home.html", {"devices": devices})


@login_required
def filters_view(request, device_token):
    device = get_object_or_404(Device, device_token=device_token, owner=request.user)
    triggers = Trigger.objects.filter(device=device)

    active_themes = set(t.category for t in triggers if not t.keyword)
    keywords = [t for t in triggers if t.keyword]

    if request.method == "POST":
        Trigger.objects.filter(device=device).delete()

        for kw in request.POST.getlist("keywords"):
            kw = kw.strip()
            if kw:
                Trigger.objects.create(device=device, keyword=kw, category="keyword")

        for theme_key, *_ in RISK_THEMES:
            if theme_key in request.POST.getlist("themes"):
                Trigger.objects.create(device=device, keyword="", category=theme_key)

        return redirect("dashboard:filters", device_token=device_token)

    return render(request, "dashboard/filters.html", {
        "device": device,
        "risk_themes": RISK_THEMES,
        "active_themes": active_themes,
        "keywords": [t.keyword for t in keywords],
    })


def api_docs(request):
    return render(request, "dashboard/api_docs.html")


@login_required
def alerts_view(request, device_token):
    device = get_object_or_404(Device, device_token=device_token, owner=request.user)
    all_alerts = list(Alert.objects.filter(device=device)[:100])

    # Enriquece cada alerta com pode_ser e recomendacoes da literatura
    for alert in all_alerts:
        info = get_risk_info(alert.category)
        alert.pode_ser      = info["pode_ser"]
        alert.recomendacoes = info["recomendacoes"]

    altos     = [a for a in all_alerts if a.risk_level == "high_risk"]
    moderados = [a for a in all_alerts if a.risk_level == "attention"]
    baixos    = [a for a in all_alerts if a.risk_level == "safe"]

    return render(request, "dashboard/alerts.html", {
        "device":        device,
        "alerts":        all_alerts,
        "altos":         altos,
        "moderados":     moderados,
        "baixos":        baixos,
        "alto_count":    len(altos),
        "moderado_count":len(moderados),
        "baixo_count":   len(baixos),
    })
