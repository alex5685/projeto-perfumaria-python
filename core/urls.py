from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

# ---- Endpoints de diagnóstico S3 (opcionais em produção) ----
import boto3
from botocore.exceptions import ClientError

def whoami_s3(request):
    try:
        sts = boto3.client("sts", region_name=settings.AWS_DEFAULT_REGION)
        return JsonResponse(sts.get_caller_identity())
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

def probe_s3(request):
    try:
        s3 = boto3.client("s3", region_name=settings.AWS_DEFAULT_REGION)
        key = "media/produtos/_probe.txt"
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=b"ok",
            ContentType="text/plain",
            ACL="public-read",
        )
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{key}"
        return JsonResponse({"ok": True, "url": url, "key": key})
    except ClientError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

def s3_put(request):
    try:
        s3 = boto3.client("s3", region_name=settings.AWS_DEFAULT_REGION)
        key = "media/produtos/_diag.txt"
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=b"diag",
            ContentType="text/plain",
            ACL="public-read",
        )
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{key}"
        return JsonResponse({"ok": True, "url": url, "key": key})
    except ClientError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

def s3_list(request):
    try:
        s3 = boto3.client("s3", region_name=settings.AWS_DEFAULT_REGION)
        prefix = "media/produtos/"
        resp = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=prefix)
        keys = []
        for it in resp.get("Contents", []):
            keys.append(it["Key"])
        return JsonResponse({"ok": True, "count": len(keys), "keys": keys})
    except ClientError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)
# --------------------------------------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),  # <-- precisa do import acima
    path('whoami-s3/', whoami_s3),
    path('probe-s3/', probe_s3),
    path('s3-put/', s3_put),
    path('s3-list/', s3_list),

    # suas rotas de app (ex.: loja) se existirem:
    # path('', include('loja.urls')),
]

# servir media em dev (não afeta Render/Docker)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
