#!/usr/bin/env bash
set -e

# Ajuste a variável de settings se necessário
export DJANGO_SETTINGS_MODULE=core.settings

echo ">> Executando migrações..."
python manage.py migrate --noinput

echo ">> Iniciando Gunicorn..."
exec gunicorn core.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 3 \
  --timeout 120
