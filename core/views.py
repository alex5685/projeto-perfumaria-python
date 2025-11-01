import json
from datetime import datetime
from typing import List

import boto3
from botocore.exceptions import ClientError, BotoCoreError

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model


# ---------- Helpers S3 ----------

def _s3_client():
    return boto3.client(
        "s3",
        region_name=settings.AWS_DEFAULT_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def _bucket_key(key_name: str) -> str:
    """Gera a chave final com o prefixo configurado."""
    prefix = settings.AWS_MEDIA_PREFIX  # ex.: media/produtos/
    return f"{prefix}{key_name}".replace("//", "/")


# ---------- Views de diagnóstico S3 ----------

def whoami_s3(request):
    """Retorna identidade do STS para confirmar credenciais / região."""
    try:
        sts = boto3.client(
            "sts",
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        ident = sts.get_caller_identity()
        return JsonResponse({"ok": True, **ident})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})


def s3_put(request):
    """Escreve um arquivo de teste no prefixo configurado."""
    key = _bucket_key("_diag.txt")
    body = f"diag @ {datetime.utcnow().isoformat()}Z"
    try:
        s3 = _s3_client()
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="text/plain",
        )
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{key}"
        return JsonResponse({"ok": True, "url": url, "key": key})
    except (ClientError, BotoCoreError) as e:
        return JsonResponse({"ok": False, "error": str(e)})


def probe_s3(request):
    """Escreve um _diag_runtime.txt (útil para checar permissões em runtime)."""
    key = _bucket_key("_diag_runtime.txt")
    body = f"runtime @ {datetime.utcnow().isoformat()}Z"
    try:
        s3 = _s3_client()
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="text/plain",
        )
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{key}"
        return JsonResponse({"ok": True, "url": url})
    except (ClientError, BotoCoreError) as e:
        return JsonResponse({"ok": False, "error": str(e)})


def s3_list(request):
    """Lista objetos do prefixo configurado."""
    prefix = settings.AWS_MEDIA_PREFIX
    try:
        s3 = _s3_client()
        resp = s3.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=prefix,
            Delimiter=None,
            MaxKeys=1000,
        )
        keys: List[str] = []
        for obj in resp.get("Contents", []):
            keys.append(obj["Key"])
        return JsonResponse({"ok": True, "count": len(keys), "keys": keys})
    except (ClientError, BotoCoreError) as e:
        return JsonResponse({"ok": False, "error": str(e)})


def s3_diag(request):
    """
    Diagnóstico completo do S3:
      - STS identity
      - Localização do bucket
      - HEAD no bucket
      - PUT de teste
      - LIST no prefixo
    """
    out = {
        "ok": True,
        "env": {
            "AWS_ACCESS_KEY_ID": (settings.AWS_ACCESS_KEY_ID[:4] + "***") if settings.AWS_ACCESS_KEY_ID else "",
            "AWS_SECRET_ACCESS_KEY": "***" if settings.AWS_SECRET_ACCESS_KEY else "",
            "AWS_DEFAULT_REGION env": settings.AWS_DEFAULT_REGION,
            "bucket": settings.AWS_STORAGE_BUCKET_NAME,
        },
        "checks": [],
    }

    try:
        sts = boto3.client(
            "sts",
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        ident = sts.get_caller_identity()
        out["checks"].append({"step": "sts.get_caller_identity", "ok": True, "identity": ident})
    except Exception as e:
        out["ok"] = False
        out["checks"].append({"step": "sts.get_caller_identity", "ok": False, "error": str(e)})
        return JsonResponse(out)

    try:
        s3 = _s3_client()
        loc = s3.get_bucket_location(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        out["checks"].append({"step": "s3.get_bucket_location", "ok": True, "bucket_location": loc})
    except (ClientError, BotoCoreError) as e:
        out["ok"] = False
        out["checks"].append({"step": "s3.get_bucket_location", "ok": False, "error": str(e)})
        return JsonResponse(out)

    try:
        s3 = _s3_client()
        head = s3.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        out["checks"].append({"step": "s3.head_bucket", "ok": True})
    except (ClientError, BotoCoreError) as e:
        out["ok"] = False
        out["checks"].append({"step": "s3.head_bucket", "ok": False, "error": str(e)})
        return JsonResponse(out)

    # put de teste
    try:
        key = _bucket_key("_diag_runtime.txt")
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=f"diag {datetime.utcnow().isoformat()}Z".encode("utf-8"),
            ContentType="text/plain",
        )
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{key}"
        out["checks"].append({"step": "s3.put_object", "key": key, "ok": True, "url": url})
    except (ClientError, BotoCoreError) as e:
        out["ok"] = False
        out["checks"].append({"step": "s3.put_object", "ok": False, "error": str(e)})
        return JsonResponse(out)

    # list no prefixo
    try:
        resp = s3.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=settings.AWS_MEDIA_PREFIX,
            MaxKeys=1000,
        )
        keys = [o["Key"] for o in resp.get("Contents", [])]
        out["checks"].append({"step": "s3.list_objects_v2", "prefix": settings.AWS_MEDIA_PREFIX, "ok": True, "count": len(keys), "keys": keys[:20]})
    except (ClientError, BotoCoreError) as e:
        out["ok"] = False
        out["checks"].append({"step": "s3.list_objects_v2", "ok": False, "error": str(e)})

    return JsonResponse(out)


# ---------- Views de manutenção / bootstrap do admin ----------

def whoami_admin(request):
    """
    Mostra se o token ADMIN_MAINT_TOKEN está carregado (sem expor o valor).
    """
    tok = (settings.ADMIN_MAINT_TOKEN or "").strip()
    return JsonResponse({"ok": bool(tok), "len": len(tok)})


def admin_bootstrap(request, token: str):
    """
    Cria (ou reseta a senha) de um superusuário de forma controlada por token.
    Exemplo:
      /admin-bootstrap/adm-Reset-9f2c/?u=Alex5685&p=Tata%26Duda929&email=alex5685%40gmail.com
    Recomendação: remover a env ADMIN_MAINT_TOKEN e/ou a rota após uso.
    """
    expected = (settings.ADMIN_MAINT_TOKEN or "").strip()
    if not expected or token != expected:
        return HttpResponse("forbidden", status=403)

    username = (request.GET.get("u") or "").strip()
    password = (request.GET.get("p") or "").strip()
    email = (request.GET.get("email") or "").strip()

    if not username or not password:
        return JsonResponse({"ok": False, "error": "missing u/p"}, status=400)

    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )
    if not created:
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True

    user.set_password(password)
    user.save()

    return JsonResponse({"ok": True, "created": created, "username": user.username, "email": user.email})
