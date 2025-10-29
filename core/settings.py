"""
Django settings for core project.
Produção no Render + Postgres + S3 (mídia) + WhiteNoise (estáticos).
"""
import os
from pathlib import Path
import dj_database_url

# ---------------------------------------
# Paths
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# Segurança / Debug
# ---------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "change-me-in-production"
)

DEBUG = os.environ.get("DEBUG", "0") in ("1", "true", "True")

# ALLOWED_HOSTS pode ser passado como string separada por vírgulas no Render
_env_hosts = os.environ.get("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h.strip() for h in _env_hosts.split(",") if h.strip()] or [
    "localhost", "127.0.0.1", ".onrender.com"
]

# CSRF confiável para Render
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

# Em proxies (Render) – informar ao Django que a origem é HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ---------------------------------------
# Aplicativos
# ---------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "loja",
    "storages",  # S3
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise precisa vir logo após SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationM
