"""
Django settings for core project.
"""
import os
from pathlib import Path
import dj_database_url # Necessário para ler a DATABASE_URL
# from decouple import config # Comentado, use se for usar django-decouple

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
# Use uma variável de ambiente no Render para a chave real (como a SECRET_KEY atual)
SECRET_KEY = os.environ.get("SECRET_KEY", "cCRnpmq9bxcH9fQQ_STL452iI9XTYOYcOaZIaPwN_t0TdI2coe9KgwzBFTtChwGBMtA") 

# SECURITY WARNING: don't run with debug turned on in production!
# Mantenha como True para ver a tela de erro detalhada no Render
DEBUG = True 

ALLOWED_HOSTS = [
    '.onrender.com', # Permite todos os subdomínios .onrender.com
    'localhost', # Para testes locais
    '127.0.0.1', # Para testes locais
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
    "whitenoise.middleware.WhiteNoiseMiddleware", # Para servir arquivos estáticos no Render
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database

# CONFIGURAÇÃO DE BANCO DE DADOS (USANDO VARIAVEL DE AMBIENTE)
if 'DATABASE_URL' in os.environ:
    # Em produção (Render), usa a variavel DATABASE_URL para PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Localmente (sem a variavel), usa SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
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
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

# Local onde Django buscará os arquivos estáticos (CSS, JS, imagens do Admin)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'


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

# 1. Leitura Explícita das Chaves de Acesso
# Mantemos a leitura explícita para garantir, embora o Boto3 as leia automaticamente do ambiente Render.
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Força a região correta (us-east-2) e o nome do bucket
AWS_S3_REGION_NAME = 'us-east-2' # Força a região correta (Alternativa 3)
AWS_STORAGE_BUCKET_NAME = 'perfumaria-fotos-alex'
AWS_LOCATION = 'media' # Prefixo para o caminho dos arquivos no S3

# Se as variáveis S3 estiverem definidas (em produção)
if AWS_STORAGE_BUCKET_NAME:
    
    # Define o S3 como o local padrão para upload de arquivos (usando a classe mais moderna)
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # CRUCIAL: Força a ACL 'public-read'. ISSO REQUER ACLs HABILITADAS no bucket S3.
    AWS_S3_OBJECT_PARAMETERS = {'ACL': 'bucket-owner-full-control'}
    
    # Configurações de acesso e segurança
    AWS_S3_FILE_OVERWRITE = False
    
    # Monta o domínio completo para que o Django use para servir as fotos
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    
    # A URL que os templates usarão (incluindo o prefixo media/)
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/' 

else:
    # Configuração de fallback para desenvolvimento local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
