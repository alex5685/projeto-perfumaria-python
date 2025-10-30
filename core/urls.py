# core/urls.py
from django.urls import path
from django.http import JsonResponse
from django.conf import settings
import boto3, botocore

def s3_list(request):
    s3 = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
    try:
        resp = s3.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=f"{settings.AWS_LOCATION}/produtos/"
        )
        keys = [x["Key"] for x in resp.get("Contents", [])]
        return JsonResponse({"ok": True, "count": len(keys), "keys": keys})
    except botocore.exceptions.ClientError as e:
        return JsonResponse({"ok": False, "where": "list", "error": str(e)}, status=500)

def s3_put(request):
    s3 = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
    key = f"{settings.AWS_LOCATION}/produtos/_diag.txt"
    try:
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=b"hello from putobject",
            ContentType="text/plain"
        )
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{key}"
        return JsonResponse({"ok": True, "url": url, "key": key})
    except botocore.exceptions.ClientError as e:
        return JsonResponse({"ok": False, "where": "put", "error": str(e)}, status=500)

urlpatterns = [
    # … suas rotas já existentes …
    path('admin/', admin.site.urls),
    path("s3-put/", s3_put, name="s3_put"),
    path("s3-list/", s3_list, name="s3_list"),
]
