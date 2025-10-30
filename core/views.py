# --- DIAGNÓSTICO S3 TEMPORÁRIO ---
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
import boto3
import datetime

@require_GET
def s3_diag(request):
    region = getattr(settings, "AWS_S3_REGION_NAME", None) or getattr(settings, "AWS_DEFAULT_REGION", None) or "us-east-2"
    bucket = settings.AWS_STORAGE_BUCKET_NAME

    out = {"region": region, "bucket": bucket}

    # 1) Quem sou (STS)
    try:
        sts = boto3.client("sts", region_name=region)
        who = sts.get_caller_identity()
        out["sts_arn"] = who.get("Arn")
        out["sts_account"] = who.get("Account")
    except Exception as e:
        out["sts_error"] = str(e)

    # 2) HeadBucket (região/permissão)
    try:
        s3 = boto3.client("s3", region_name=region)
        s3.head_bucket(Bucket=bucket)
        out["head_bucket_ok"] = True
    except Exception as e:
        out["head_bucket_error"] = str(e)

    # 3) PutObject em media/produtos/_diag.txt
    key = "media/produtos/_diag.txt"
    try:
        body = f"diag {datetime.datetime.utcnow().isoformat()}Z\n"
        s3.put_object(Bucket=bucket, Key=key, Body=body.encode("utf-8"), ContentType="text/plain")
        out["put_object_ok"] = True
        out["put_object_url"] = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
    except Exception as e:
        out["put_object_error"] = str(e)

    # 4) ListObjectsV2 no prefixo
    try:
        resp = s3.list_objects_v2(Bucket=bucket, Prefix="media/produtos/", MaxKeys=20)
        out["list_count"] = resp.get("KeyCount", 0)
        out["list_keys"] = [it["Key"] for it in resp.get("Contents", [])]
    except Exception as e:
        out["list_error"] = str(e)

    return JsonResponse(out)
