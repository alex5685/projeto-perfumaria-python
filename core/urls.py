from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.conf import settings
import boto3
from botocore.config import Config

def healthz(_):
    return JsonResponse({"ok": True})

def whoami_s3(_):
    try:
        sts = boto3.client("sts", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-2"))
        ident = sts.get_caller_identity()
        return JsonResponse({"ok": True, **ident})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})

def s3_diag(_):
    out = {"ok": True, "env": {} , "settings": {}, "checks": []}
    try:
        out["env"]["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID", "AKIA***")
        out["env"]["AWS_SECRET_ACCESS_KEY"] = "****"
        out["env"]["region"] = os.getenv("AWS_DEFAULT_REGION", "us-east-2")
        bucket = os.getenv("AWS_STORAGE_BUCKET_NAME", "")
        out["settings"] = {
            "AWS_STORAGE_BUCKET_NAME": bucket,
            "AWS_DEFAULT_REGION": os.getenv("AWS_DEFAULT_REGION", "<missing>"),
            "DEBUG": settings.DEBUG,
        }
        cfg = Config(region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-2"))
        s3 = boto3.client("s3", config=cfg)
        sts = boto3.client("sts", config=cfg)

        # 1) STS
        ident = sts.get_caller_identity()
        out["checks"].append({"step":"sts.get_caller_identity","ok":True,"identity":ident})

        # 2) bucket location
        loc = s3.get_bucket_location(Bucket=bucket)
        out["checks"].append({"step":"s3.get_bucket_location","ok":True,"bucket_location":loc})

        # 3) head bucket
        s3.head_bucket(Bucket=bucket)
        out["checks"].append({"step":"s3.head_bucket","ok":True})

        # 4) put object
        key = "media/produtos/_diag_runtime.txt"
        s3.put_object(Bucket=bucket, Key=key, Body=b"ok")
        out["checks"].append({"step":"s3.put_object","ok":True,"key":key,"url":f"https://{bucket}.s3.{out['env']['region']}.amazonaws.com/{key}"})

        # 5) list
        resp = s3.list_objects_v2(Bucket=bucket, Prefix="media/produtos/")
        keys = []
        for it in resp.get("Contents", []):
            keys.append(it["Key"])
        out["checks"].append({"step":"s3.list_objects_v2","ok":True,"count":len(keys),"keys":keys})
        return JsonResponse(out)
    except Exception as e:
        out["ok"] = False
        out["error"] = str(e)
        return JsonResponse(out)

urlpatterns = [
    path("healthz/", healthz, name="healthz"),
    path("whoami-s3/", whoami_s3, name="whoami-s3"),
    path("s3-diag/", s3_diag, name="s3-diag"),
    path("admin/", admin.site.urls),
]
