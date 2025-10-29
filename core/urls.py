from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
import os, boto3
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def whoami_s3(request):
    sts = boto3.client(
        "sts",
        region_name=os.environ.get("AWS_S3_REGION_NAME") or os.environ.get("AWS_DEFAULT_REGION", "us-east-2"),
    )
    return JsonResponse(sts.get_caller_identity())

def probe_s3(request):
    name = "produtos/_probe.txt"  # ficará em media/produtos/_probe.txt
    default_storage.save(name, ContentFile(b"hello s3"))
    return JsonResponse({"ok": True, "url": default_storage.url(name)})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("whoami-s3/", whoami_s3),
    path("probe-s3/", probe_s3),
]
