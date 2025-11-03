# core/settings.py
from pathlib import Path
import os
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------------------
# Básico
# --------------------------------------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-prod")
DEBUG = os.environ.get("DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    "localhost", "127.0.0.1",
    ".onrender.com",
]

# Para construir os trusted origins automaticamente quando em onrender.com
_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
CSRF_TRUSTED_ORIGINS = [
    "https://localhost",
    "https://*.onrender.com",
]
if _render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{_render_host}")

# --------------------------------------------------------------------------------------
# Apps
# --------------------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",     # << necessário para o collectstatic

    # Terceiros
    "storages",                       # django-storages (S3)

    # Apps do projeto
    "loja",
]

# --------------------------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # << servir estáticos no Render
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

# --------------------------------------------------------------------------------------
# Banco de dados: DATABASE_URL (Postgres no Render) com fallback SQLite
# --------------------------------------------------------------------------------------
# Exemplos de DATABASE_URL:
#  - Postgres:  postgres://user:pass@host:5432/dbname
#  - Render    (variável DATABASE_URL já pronta)
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --------------------------------------------------------------------------------------
# Idioma/Timezone
# --------------------------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------------------
# Arquivos estáticos (WhiteNoise) e mídia (S3)
# --------------------------------------------------------------------------------------
# ESTÁTICOS → WhiteNoise (build do Render roda "collectstatic")
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# (opcional, caso tenha pasta "static" no projeto)
# STATICFILES_DIRS = [BASE_DIR / "static"]

# MÍDIA → S3 (django-storages/boto3)
# OBS: deixe estáticos no WhiteNoise e use S3 apenas para uploads (ImageField/FileField)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-2")  # ajuste se necessário

# Só ativa S3 se as credenciais existirem
USE_S3_MEDIA = all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME])

if USE_S3_MEDIA:
    # Endpoint automático pela região; se usar outro (ex.: CloudFront), defina AWS_S3_CUSTOM_DOMAIN
    AWS_S3_REGION_NAME = AWS_DEFAULT_REGION
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_QUERYSTRING_AUTH = False  # URLs públicas de mídia (ajuste conforme sua política)
    AWS_S3_FILE_OVERWRITE = False
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    # Fallback local (desenvolvimento)
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------------------------------------------
# Segurança / Proxy (Render)
# --------------------------------------------------------------------------------------
# Respeitar o X-Forwarded-Proto do proxy para detectar HTTPS corretamente
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

# Se quiser forçar HTTPS em produção:
if not DEBUG:
    SECURE_SSL_REDIRECT = True

# --------------------------------------------------------------------------------------
# Senhas / Validators
# --------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------------------------
# Admin
# --------------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
