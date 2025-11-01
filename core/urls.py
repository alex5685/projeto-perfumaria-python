from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Admin Django
    path("admin/", admin.site.urls),

    # ---- Diagnósticos S3 ----
    path("whoami-s3/", views.whoami_s3, name="whoami_s3"),
    path("s3-diag/", views.s3_diag, name="s3_diag"),
    path("s3-put/", views.s3_put, name="s3_put"),
    path("s3-list/", views.s3_list, name="s3_list"),
    path("probe-s3/", views.probe_s3, name="probe_s3"),

    # ---- Manutenção / Bootstrap do admin ----
    path("whoami-admin/", views.whoami_admin, name="whoami_admin"),
    path("admin-bootstrap/<str:token>/", views.admin_bootstrap, name="admin_bootstrap"),
]
