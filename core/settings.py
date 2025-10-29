"""
Django settings for core project.
"""
import os
from pathlib import Path
import dj_database_url 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# Chave Secreta: Lida de forma segura via variável de ambiente no Render.
SECRET_KEY = os.environ.get("SECRET_KEY", "cCRnpmq9bxcH9fQQ_STL452iI9XTYOYcOaZIaPwN_t0TdI2coe9KgwzBFTtChwGBMtA") 

# DEBUG: Lida de forma segura via variável de ambiente.
DEBUG = os.environ.get("DEBUG", "True") == "True" 

ALLOWED_HOSTS = [
    '.onrender.com', # Permite todos os subdomínios .onrender.com
    'localhost',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "loja",
    "storages", # ADICIONADO para S3
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # CORREÇÃO: Para servir estáticos
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')], # Re-adicionado para garantir
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


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Sao_Paulo" # Fuso horário brasileiro
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# Configuração para arquivos estáticos (CSS/JS) no Render
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# SEGURANÇA E ARQUIVOS DE MÍDIA (CSRF/COOKIES/S3)
# ----------------------------------------------------------------------

# Adicione a URL base do seu serviço Render à lista de origens confiáveis
CSRF_TRUSTED_ORIGINS = ['https://projeto-perfumaria-python.onrender.com']

# CONFIGURAÇÕES DE COOKIES PARA PRODUÇÃO (Obrigatório em HTTPS/Render)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# CONFIGURAÇÕES DO AWS S3 (PARA ARQUIVOS DE MÍDIA)

# Força a região correta (us-east-2) e o nome do bucket
AWS_S3_REGION_NAME = 'us-east-2' 
AWS_STORAGE_BUCKET_NAME = 'perfumaria-fotos-alex'
AWS_LOCATION = 'media' # Prefixo para o caminho dos arquivos no S3

# Se o nome do bucket estiver definido (em produção)
if AWS_STORAGE_BUCKET_NAME:
    
    # Define o S3 como o local padrão para upload de arquivos (usando a classe moderna)
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # ÚLTIMA TENTATIVA: Voltamos para 'public-read' APÓS desativar o bloqueio de ACLs no S3.
    AWS_S3_OBJECT_PARAMETERS = {'ACL': 'public-read'} 
    
    # Configurações de acesso e segurança
    AWS_S3_FILE_OVERWRITE = False
    
    # Monta o domínio completo
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    
    # A URL que os templates usarão
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

else:
    # Configuração de fallback para desenvolvimento local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
