import os
import json
import boto3
from botocore.client import Config
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# Helpers seguros para região/bucket
def _env_region():
    # 1) env, 2) settings alias, 3) settings principal, 4) fallback
    return (
        os.getenv("AWS_DEFAULT_REGION")
        or os.getenv("AWS_REGION")
        or getattr(settings, "AWS_S3_REGION_NAME", None)
        or getattr(settings, "AWS_DEFAULT_REGION", None)
        or "us-east-2"
    )

def _bucket():
    return (
        os.getenv("AWS_STORAGE_BUCKET_NAME")
        or getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")
    )

def _s3_client(region=None):
    region = region or _env_region()
    return boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", getattr(settings, "AWS_ACCESS_KEY_ID", "")),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", getattr(settings, "AWS_SECRET_ACCESS_KEY", "")),
        config=Config(s3={"addressing_style": "virtual"}),
    )

@require_GET
def whoami_s3(request):
    try:
        sts = boto3.client(
            "sts",
            region_name=_env_region(),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", getattr(settings, "AWS_ACCESS_KEY_ID", "")),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", getattr(settings, "AWS_SECRET_ACCESS_KEY", "")),
        )
        ident = sts.get_caller_identity()
        return JsonResponse({"ok": True, **ident})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})

@require_GET
def s3_put(request):
    try:
        region = _env_region()
        bucket = _bucket()
        key = "media/produtos/_diag.txt"
        body = f"ok {_env_region()}".encode()

        s3 = _s3_client(region)
        s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="text/plain")

        url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
        return JsonResponse({"ok": True, "url": url, "key": key})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})

@require_GET
def s3_list(request):
    try:
        region = _env_region()
        bucket = _bucket()
        prefix = "media/produtos/"
        s3 = _s3_client(region)

        keys = []
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for item in page.get("Contents", []):
                keys.append(item["Key"])

        return JsonResponse({"ok": True, "count": len(keys), "keys": keys})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})

@require_GET
def probe_s3(request):
    # PUT de um arquivo com timestamp — simples para validar escrita
    try:
        region = _env_region()
        bucket = _bucket()
        key = "media/produtos/_diag_runtime.txt"
        body = f"written at runtime (region={region})".encode()

        s3 = _s3_client(region)
        s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="text/plain")
        url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
        return JsonResponse({"ok": True, "url": url})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})

@require_GET
def s3_diag(request):
    """Diagnóstico encadeado: STS → localização → HEAD no bucket → PUT → LIST"""
    out = {"ok": True, "env": {
        "AWS_ACCESS_KEY_ID": f"{os.getenv('AWS_ACCESS_KEY_ID','')[:4]}***",
        "AWS_SECRET_ACCESS_KEY": "***" if os.getenv("AWS_SECRET_ACCESS_KEY") else "",
        "AWS_DEFAULT_REGION env": os.getenv("AWS_DEFAULT_REGION"),
    }, "settings": {
        "AWS_STORAGE_BUCKET_NAME": getattr(settings, "AWS_STORAGE_BUCKET_NAME", "<missing>"),
        "AWS_DEFAULT_REGION": getattr(settings, "AWS_DEFAULT_REGION", "<missing>"),
    }, "DEBUG": settings.DEBUG}

    region = _env_region()
    bucket = _bucket()
    out["region"] = region
    out["bucket"] = bucket

    try:
        sts = boto3.client(
            "sts",
            region_name=region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", getattr(settings, "AWS_ACCESS_KEY_ID", "")),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", getattr(settings, "AWS_SECRET_ACCESS_KEY", "")),
        )
        ident = sts.get_caller_identity()
        out["checks"] = [{"step": "sts.get_caller_identity", "ok": True, "identity": ident}]
    except Exception as e:
        out["ok"] = False
        out["checks"] = [{"step": "sts.get_caller_identity", "ok": False, "error": str(e)}]
        return JsonResponse(out)

    s3 = _s3_client(region)

    # get_bucket_location
    try:
        loc = s3.get_bucket_location(Bucket=bucket)
        out["checks"].append({"step": "s3.get_bucket_location", "ok": True, "bucket_location": loc})
    except Exception as e:
        out["ok"] = False
        out["checks"].append({"step": "s3.get_bucket_location", "ok": False, "error": str(e)})
        return JsonResponse(out)

    # head_bucket
    try:
        hb = s3.head_bucket(Bucket=bucket)
        out["checks"].append({"step": "s3.head_bucket", "ok": True})
    except Exception as e:
        out["ok"] = False
        out["checks"].append({"step": "s3.head_bucket", "ok": False, "error": str(e)})
        return JsonResponse(out)

    # put + list
    try:
        key = "media/produtos/_diag_runtime.txt"
        body = f"diag write (region={region})".encode()
        s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="text/plain")
        url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
        out["checks"].append({"step": "s3.put_object", "key": key, "ok": True, "url": url})
    except Exception as e:
        out["ok"] = False
        out["checks"].append({"step": "s3.put_object", "ok": False, "error": str(e)})
        return JsonResponse(out)

    try:
        prefix = "media/produtos/"
        keys = []
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for item in page.get("Contents", []):
                keys.append(item["Key"])
        out["checks"].append({"step": "s3.list_objects_v2", "prefix": prefix, "ok": True, "count": len(keys), "keys": keys[:10]})
    except Exception as e:
        out["ok"] = False
        out["checks"].append({"step": "s3.list_objects_v2", "ok": False, "error": str(e)})

    return JsonResponse(out)
