import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------
# SEGREDOS / DEBUG / HOSTS
# ---------------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = [
    "projeto-perfumaria-python.onrender.com",
    "localhost",
    "127.0.0.1",
]

# ---------------------------------------------------------------------
# SEGURANÇA / PROXY / CSRF
# ---------------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://projeto-perfumaria-python.onrender.com",
    "https://*.onrender.com",
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# ---------------------------------------------------------------------
# APPS
# ---------------------------------------------------------------------
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

# ---------------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ---------------------------------------------------------------------
# DB (mantenho sqlite; se usar Postgres do Render, troque aqui)
# ---------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------------------
# ESTÁTICOS / MÍDIA (WhiteNoise + S3 para uploads)
# ---------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------------
# AWS S3 (django-storages)
# ---------------------------------------------------------------------
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "perfumaria-fotos-alex")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-2")

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_DEFAULT_REGION}.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# ---------------------------------------------------------------------
# I18N
# ---------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------------
LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/admin/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

import os
ADMIN_MAINT_TOKEN = os.environ.get("ADMIN_MAINT_TOKEN", "").strip()
