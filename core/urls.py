from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # Admin bootstrap (emergência) – dois formatos:
    path("admin-bootstrap/", views.admin_bootstrap_qs, name="admin_bootstrap_qs"),
    path("admin-bootstrap/<str:token>/", views.admin_bootstrap_path, name="admin_bootstrap_path"),
]
