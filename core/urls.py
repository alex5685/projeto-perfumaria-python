from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # diagnósticos S3
    path("whoami-s3/", views.whoami_s3, name="whoami-s3"),
    path("s3-diag/", views.s3_diag, name="s3-diag"),
    path("s3-put/", views.s3_put, name="s3-put"),
    path("s3-list/", views.s3_list, name="s3-list"),
    path("probe-s3/", views.probe_s3, name="probe-s3"),
]
