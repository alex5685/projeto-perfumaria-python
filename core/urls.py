# core/urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core import views  # <- usamos as views acima

urlpatterns = [
    path("admin/", admin.site.urls),

    # Diagnósticos S3
    path("whoami-s3/", views.whoami_s3, name="whoami-s3"),
    path("s3-put/", views.s3_put, name="s3-put"),
    path("probe-s3/", views.probe_s3, name="probe-s3"),
    path("s3-list/", views.s3_list, name="s3-list"),
    path("s3-diag/", views.s3_diag, name="s3-diag"),
]

# Em DEV, servir media local (não interfere no Render)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
