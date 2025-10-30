import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    *[h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()],
    "localhost", "127.0.0.1",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # sua app:
    "loja",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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

# Banco de dados (Render → variáveis de ambiente já apontam)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # dj-database-url não é estritamente necessário aqui; use seu config atual se preferir
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------- S3 / boto3 ----------
# Estes três devem existir no Render
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "")

# A REGIÃO era o que faltava no settings
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-2")  # Ohio (igual ao console)
# Muitos pacotes esperam este alias:
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", AWS_DEFAULT_REGION)

# Opcionalmente, para URLs públicas legíveis e sem assinatura
AWS_QUERYSTRING_AUTH = False
AWS_S3_ADDRESSING_STYLE = "virtual"

# Se você usa django-storages (FileSystem local para estático e S3 p/ media)
USE_S3_FOR_MEDIA = True
if USE_S3_FOR_MEDIA and AWS_STORAGE_BUCKET_NAME:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    # Pasta de mídia dentro do bucket
    AWS_LOCATION = "media"
    AWS_DEFAULT_ACL = None
    # (o path “media/” é tratado na aplicação; as views que criamos já usam media/produtos/)
# ---------- /S3 ----------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
