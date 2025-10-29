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
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
DEBUG = os.environ.get("DEBUG", "0") in ("1", "true", "True")

_env_hosts = os.environ.get("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h.strip() for h in _env_hosts.split(",") if h.strip()] or [
    "localhost", "127.0.0.1", ".onrender.com"
]

CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ---------------------------------------
# Apps
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
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise logo após SecurityMiddleware
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

# ---------------------------------------
# Banco (Render Postgres)
# ---------------------------------------
DEFAULT_DB_URL = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL", DEFAULT_DB_URL),
        conn_max_age=600,
        ssl_require=True if os.environ.get("DATABASE_URL", "").startswith("postgres") else False,
    )
}

# ---------------------------------------
# Locale
# ---------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ---------------------------------------
# Estáticos (WhiteNoise)
# ---------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------
# Mídia (S3)
# ---------------------------------------
USE_S3 = os.environ.get("USE_S3", "1") in ("1", "true", "True")

if USE_S3:
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME") or os.environ.get("AWS_DEFAULT_REGION", "us-east-2")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "perfumaria-fotos-alex")
    AWS_LOCATION = os.environ.get("AWS_LOCATION", "media")

    AWS_DEFAULT_ACL = None          # não grava ACL por objeto
    AWS_QUERYSTRING_AUTH = False    # URLs públicas sem assinatura
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------
# Logs
# ---------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO" if not DEBUG else "DEBUG"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
