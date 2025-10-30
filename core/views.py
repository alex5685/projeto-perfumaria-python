# core/views.py
from django.http import JsonResponse
from django.conf import settings

import os
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError


def _public_url(bucket: str, region: str, key: str) -> str:
    # Formato de URL padrão para S3 (region explícita)
    return f"https://{bucket}.s3.{region}.amazonaws.com/{key}"


def whoami_s3(request):
    """Retorna a identidade AWS (STS) usada pela aplicação."""
    try:
        sts = boto3.client("sts", region_name=settings.AWS_DEFAULT_REGION)
        ident = sts.get_caller_identity()
        return JsonResponse({"ok": True, "identity": ident})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


def s3_put(request):
    """Grava um arquivo de diagnóstico: media/produtos/_diag.txt (ACL public-read)."""
    key = "media/produtos/_diag.txt"
    try:
        s3 = boto3.client("s3", region_name=settings.AWS_DEFAULT_REGION)
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=b"diag",
            ContentType="text/plain",
            ACL="public-read",
        )
        return JsonResponse(
            {
                "ok": True,
                "key": key,
                "url": _public_url(settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_DEFAULT_REGION, key),
            }
        )
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


def probe_s3(request):
    """Grava um arquivo de teste: media/produtos/_probe.txt (ACL public-read)."""
    key = "media/produtos/_probe.txt"
    try:
        s3 = boto3.client("s3", region_name=settings.AWS_DEFAULT_REGION)
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=b"ok",
            ContentType="text/plain",
            ACL="public-read",
        )
        return JsonResponse(
            {
                "ok": True,
                "key": key,
                "url": _public_url(settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_DEFAULT_REGION, key),
            }
        )
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


def s3_list(request):
    """Lista objetos sob o prefixo media/produtos/."""
    prefix = "media/produtos/"
    try:
        s3 = boto3.client("s3", region_name=settings.AWS_DEFAULT_REGION)
        resp = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=prefix)
        keys = [it["Key"] for it in resp.get("Contents", [])]
        return JsonResponse({"ok": True, "count": len(keys), "keys": keys})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


def s3_diag(request):
    """
    Diagnóstico completo para 500:
      - mostra variáveis críticas
      - valida STS (credenciais)
      - valida bucket e região
      - HEAD no bucket
      - PUT de um arquivo teste
      - LIST no prefixo
    Retorna tudo em JSON para facilitar.
    """
    out = {
        "ok": False,
        "env": {
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID", "<missing>")[:6] + "...",
            "AWS_SECRET_ACCESS_KEY": "***" if os.getenv("AWS_SECRET_ACCESS_KEY") else "<missing>",
            "AWS_DEFAULT_REGION_env": os.getenv("AWS_DEFAULT_REGION", "<missing>"),
        },
        "settings": {
            "AWS_STORAGE_BUCKET_NAME": getattr(settings, "AWS_STORAGE_BUCKET_NAME", "<missing>"),
            "AWS_DEFAULT_REGION": getattr(settings, "AWS_DEFAULT_REGION", "<missing>"),
            "DEBUG": getattr(settings, "DEBUG", None),
        },
        "checks": [],
    }

    bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
    region = getattr(settings, "AWS_DEFAULT_REGION", None)

    try:
        # 1) STS - quem sou?
        step = {"step": "sts.get_caller_identity"}
        try:
            sts = boto3.client("sts", region_name=region)
            ident = sts.get_caller_identity()
            step["ok"] = True
            step["identity"] = ident
        except (NoCredentialsError, EndpointConnectionError, ClientError) as e:
            step["ok"] = False
            step["error"] = str(e)
        out["checks"].append(step)

        # 2) location do bucket
        step = {"step": "s3.get_bucket_location"}
        try:
            s3 = boto3.client("s3", region_name=region)
            loc = s3.get_bucket_location(Bucket=bucket)
            step["ok"] = True
            step["bucket_location"] = loc
        except ClientError as e:
            step["ok"] = False
            step["error"] = str(e)
        out["checks"].append(step)

        # 3) head_bucket
        step = {"step": "s3.head_bucket"}
        try:
            s3.head_bucket(Bucket=bucket)
            step["ok"] = True
        except ClientError as e:
            step["ok"] = False
            step["error"] = str(e)
        out["checks"].append(step)

        # 4) put_object (arquivo temporário de diagnóstico)
        key = "media/produtos/_diag_runtime.txt"
        step = {"step": "s3.put_object", "key": key}
        try:
            s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=b"diag-runtime",
                ContentType="text/plain",
                ACL="public-read",
            )
            step["ok"] = True
            step["url"] = _public_url(bucket, region, key)
        except ClientError as e:
            step["ok"] = False
            step["error"] = str(e)
        out["checks"].append(step)

        # 5) list_objects no prefixo
        step = {"step": "s3.list_objects_v2", "prefix": "media/produtos/"}
        try:
            resp = s3.list_objects_v2(Bucket=bucket, Prefix="media/produtos/")
            keys = [it["Key"] for it in resp.get("Contents", [])]
            step["ok"] = True
            step["count"] = len(keys)
            step["keys"] = keys
        except ClientError as e:
            step["ok"] = False
            step["error"] = str(e)
        out["checks"].append(step)

        # Se todas as etapas principais passaram, marca ok geral
        out["ok"] = all(c.get("ok") for c in out["checks"])
        return JsonResponse(out, status=200 if out["ok"] else 500)

    except Exception as e:
        out["error"] = str(e)
        return JsonResponse(out, status=500)
