"""
Django settings for core project.
"""
import os
from pathlib import Path
import dj_database_url # Necessário para ler a DATABASE_URL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "cCRnpmq9bxcH9fQQ_STL452iI9XTYOYcOaZIaPwN_t0TdI2coe9KgwzBFTtChwGBMtA") 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 
ALLOWED_HOSTS = [
    '.onrender.com', 
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
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SEGURANÇA E ARQUIVOS DE MÍDIA (CSRF/COOKIES/S3)
CSRF_TRUSTED_ORIGINS = ['https://projeto-perfumaria-python.onrender.com']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# CONFIGURAÇÕES DO AWS S3 (PARA ARQUIVOS DE MÍDIA)

# 1. Leitura Explícita das Chaves de Acesso
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Leitura das variáveis de ambiente restantes
# 5. CORREÇÃO DA REGIÃO: Prioriza AWS_DEFAULT_REGION, o padrão do Boto3.
AWS_S3_REGION_NAME = os.environ.get('AWS_DEFAULT_REGION', os.environ.get('AWS_REGION_NAME')) 
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# 4. Define o caminho interno dentro do bucket
AWS_LOCATION = 'media'

# Se as variáveis S3 estiverem definidas (ou seja, em producao)
if AWS_STORAGE_BUCKET_NAME and AWS_S3_REGION_NAME: 
    
    # 2. Mudar o Backend de Storage para S3Boto3Storage
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # 3. Parâmetro ACL Obrigatório para Propriedade do Objeto
    AWS_S3_OBJECT_PARAMETERS = {'ACL': 'bucket-owner-full-control'}
    
    # Configurações de acesso e segurança
    AWS_S3_FILE_OVERWRITE = False
    
    # Monta o domínio completo
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    
    # A URL que os templates usarão (USA o AWS_LOCATION)
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/' 

else:
    # Configuração de fallback para desenvolvimento local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
