import os
import datetime as dt

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import get_user_model


# =========================
# Helpers & Constantes
# =========================

def _get_region() -> str:
    """
    Região, com ordem de precedência:
    1) settings.AWS_DEFAULT_REGION
    2) env AWS_DEFAULT_REGION
    3) 'us-east-2' (padrão do seu bucket)
    """
    return getattr(settings, "AWS_DEFAULT_REGION", None) or \
           os.getenv("AWS_DEFAULT_REGION") or "us-east-2"


REGION = _get_region()
BUCKET = getattr(settings, "AWS_STORAGE_BUCKET_NAME", os.getenv("AWS_STORAGE_BUCKET_NAME", ""))
PREFIX = "media/produtos/"  # onde salvamos arquivos de diagnóstico


def _s3_client():
    """
    Cria um boto3.client('s3') respeitando região e timeouts razoáveis.
    """
    cfg = Config(region_name=REGION, retries={"max_attempts": 3, "mode": "standard"})
    return boto3.client(
        "s3",
        region_name=REGION,
        config=cfg,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def _obj_url(key: str) -> str:
    """
    Monta URL pública padrão do S3 (path-style por região):
    https://{bucket}.s3.{region}.amazonaws.com/{key}
    """
    return f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{key}"


# =========================
# Views de Diagnóstico S3
# =========================

def whoami_s3(request):
    """
    Retorna a identidade (STS) das credenciais em uso pelo servidor.
    Útil para detectar credenciais erradas/expiradas.
    """
    try:
        sts = boto3.client(
            "sts",
            region_name=REGION,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        resp = sts.get_caller_identity()
        return JsonResponse({"ok": True, **resp})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


def s3_diag(request):
    """
    Pipeline completo de diagnóstico:
      1) STS get_caller_identity
      2) bucket location
      3) head_bucket
      4) put objeto de runtime
      5) list prefix
    """
    out = {"ok": True, "env": {
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID", "")[:4] + "****" if os.getenv("AWS_ACCESS_KEY_ID") else "",
        "AWS_SECRET_ACCESS_KEY": "****" if os.getenv("AWS_SECRET_ACCESS_KEY") else "",
        "AWS_DEFAULT_REGION env": os.getenv("AWS_DEFAULT_REGION"),
        "region": REGION,
        "bucket": BUCKET,
    }}
    s3 = _s3_client()

    # 1) STS
    try:
        sts = boto3.client("sts", region_name=REGION)
        idt = sts.get_caller_identity()
        out["checks"] = [{"step": "sts.get_caller_identity", "ok": True, "identity": idt}]
    except Exception as e:
        out["ok"] = False
        out["checks"] = [{"step": "sts.get_caller_identity", "ok": False, "error": str(e)}]
        return JsonResponse(out, status=500)

    # 2) location
    try:
        loc = s3.get_bucket_location(Bucket=BUCKET)
        out["bucket_location"] = loc
    except Exception as e:
        out["ok"] = False
        out["bucket_location"] = {"ok": False, "error": str(e)}
        return JsonResponse(out, status=500)

    # 3) head_bucket
    try:
        s3.head_bucket(Bucket=BUCKET)
        out.setdefault("steps", []).append({"step": "s3.head_bucket", "ok": True})
    except Exception as e:
        out["ok"] = False
        out.setdefault("steps", []).append({"step": "s3.head_bucket", "ok": False, "error": str(e)})
        return JsonResponse(out, status=500)

    # 4) put object (runtime txt)
    key = f"{PREFIX}_diag_runtime.txt"
    body = f"diag @ {dt.datetime.utcnow().isoformat()}Z\nregion={REGION}\n"
    try:
        s3.put_object(Bucket=BUCKET, Key=key, Body=body.encode("utf-8"), ContentType="text/plain")
        out["steps"].append({"step": "s3.put_object", "key": key, "ok": True, "url": _obj_url(key)})
    except Exception as e:
        out["ok"] = False
        out["steps"].append({"step": "s3.put_object", "key": key, "ok": False, "error": str(e)})
        return JsonResponse(out, status=500)

    # 5) list prefix
    try:
        res = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)
        keys = [obj["Key"] for obj in res.get("Contents", [])]
        out["steps"].append({"step": "s3.list_objects_v2", "prefix": PREFIX, "ok": True, "count": len(keys), "keys": keys})
    except Exception as e:
        out["ok"] = False
        out["steps"].append({"step": "s3.list_objects_v2", "ok": False, "error": str(e)})
        return JsonResponse(out, status=500)

    return JsonResponse(out)


def s3_put(request):
    """
    Grava (ou sobrescreve) um arquivo fixo de diagnóstico.
    """
    key = f"{PREFIX}_diag.txt"
    body = f"_diag written at {dt.datetime.utcnow().isoformat()}Z"
    try:
        s3 = _s3_client()
        s3.put_object(Bucket=BUCKET, Key=key, Body=body.encode("utf-8"), ContentType="text/plain")
        return JsonResponse({"ok": True, "url": _obj_url(key), "key": key})
    except (BotoCoreError, ClientError) as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


def probe_s3(request):
    """
    Grava um arquivo cujo nome muda a cada chamada (_diag_runtime.txt)
    apenas para validar escrita.
    """
    key = f"{PREFIX}_diag_runtime.txt"
    body = f"probe @ {dt.datetime.utcnow().isoformat()}Z"
    try:
        s3 = _s3_client()
        s3.put_object(Bucket=BUCKET, Key=key, Body=body.encode("utf-8"), ContentType="text/plain")
        return JsonResponse({"ok": True, "url": _obj_url(key)})
    except (BotoCoreError, ClientError) as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


def s3_list(request):
    """
    Lista os objetos em media/produtos/.
    """
    try:
        s3 = _s3_client()
        res = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)
        keys = [c["Key"] for c in res.get("Contents", [])]
        return JsonResponse({"ok": True, "count": len(keys), "keys": keys})
    except (BotoCoreError, ClientError) as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


# =========================
# Bootstrap temporário do Admin
# =========================

def admin_bootstrap(request):
    """
    Cria/atualiza um superusuário, protegido por token de manutenção.
    Exemplo:
      /admin-bootstrap/?token=SEU_TOKEN&u=alex5685&p=NovaSenhaF0rte!&e=alex@exemplo.com

    Após usar, REMOVA:
      - esta rota de urls.py
      - esta função de views.py
      - a env var ADMIN_MAINT_TOKEN
    """
    token = request.GET.get("token")
    if not token or token != getattr(settings, "ADMIN_MAINT_TOKEN", ""):
        return HttpResponseForbidden("forbidden")

    username = request.GET.get("u", "admin")
    password = request.GET.get("p")
    email = request.GET.get("e", f"{username}@example.com")

    if not password:
        return JsonResponse({"ok": False, "error": "missing 'p' (password)"}, status=400)

    User = get_user_model()
    user, created = User.objects.get_or_create(username=username, defaults={"email": email})
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()

    return JsonResponse({
        "ok": True,
        "action": "created" if created else "updated",
        "user": username,
        "is_superuser": user.is_superuser,
        "is_staff": user.is_staff,
    })


# =========================
# Healthcheck
# =========================

def healthz(request):
    return JsonResponse({"ok": True, "status": "up"})
