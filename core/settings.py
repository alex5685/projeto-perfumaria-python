# ====== Hosts / CSRF / Proxy ======
import os

DEBUG = os.getenv("DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    "localhost", "127.0.0.1",
    # Render:
    "projeto-perfumaria-python.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://projeto-perfumaria-python.onrender.com",
    "https://*.onrender.com",
]

# Muito importante no Render (proxy HTTPS):
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ====== Cookies / Redirect ======
# Em produção, é correto manter True, mas só se o proxy estiver confiável (linha acima).
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "1") == "1"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# Opcional: evita problemas se algum header vier diferente
SECURE_REDIRECT_EXEMPT = [r"^healthz/$"]
