from django.urls import path
from . import views

app_name = "loja"

urlpatterns = [
    # Endpoints de diagnóstico
    path("diag/ping/", views.diag_ping, name="diag_ping"),
    path("diag/db/", views.diag_db, name="diag_db"),
]
