from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model
from django.conf import settings
from urllib.parse import unquote

User = get_user_model()

def _check_token_or_403(token_in):
    token_env = getattr(settings, "ADMIN_MAINT_TOKEN", "").strip()
    if not token_env or token_in.strip() != token_env:
        return False
    return True

def _upsert_superuser(username: str, password: str, email: str):
    username = (username or "").strip()
    email = (email or "").strip()
    if not username or not password:
        return {"ok": False, "error": "username and password are required"}

    user, created = User.objects.get_or_create(username=username)
    user.is_staff = True
    user.is_superuser = True
    if email:
        user.email = email
    user.set_password(password)
    user.save()
    return {"ok": True, "created": created, "username": user.username, "email": user.email}

@csrf_exempt
@require_GET
def admin_bootstrap_qs(request):
    """
    Formato: /admin-bootstrap/?token=<TOKEN>&u=<username>&p=<password>&email=<email>
    (senha deve estar URL-encodada quando tiver caracteres especiais)
    """
    token = request.GET.get("token", "")
    if not _check_token_or_403(token):
        return HttpResponseForbidden("forbidden")

    username = request.GET.get("u", "")
    password = request.GET.get("p", "")
    email = request.GET.get("email", "") or request.GET.get("e", "")
    # por garantia, decodifica (se já vier decodificado, não quebra)
    username = unquote(username)
    password = unquote(password)
    email = unquote(email)

    result = _upsert_superuser(username, password, email)
    return JsonResponse(result, status=200 if result.get("ok") else 400)

@csrf_exempt
@require_GET
def admin_bootstrap_path(request, token):
    """
    Formato alternativo: /admin-bootstrap/<TOKEN>/?u=<username>&p=<password>&email=<email>
    Útil para evitar erros de querystring.
    """
    if not _check_token_or_403(token):
        return HttpResponseForbidden("forbidden")

    username = request.GET.get("u", "")
    password = request.GET.get("p", "")
    email = request.GET.get("email", "") or request.GET.get("e", "")
    username = unquote(username)
    password = unquote(password)
    email = unquote(email)

    result = _upsert_superuser(username, password, email)
    return JsonResponse(result, status=200 if result.get("ok") else 400)
