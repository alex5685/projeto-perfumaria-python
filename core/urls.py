from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("loja.urls")),  # rotas do app (mínimas), não afeta admin
]
