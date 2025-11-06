# ====== Base ======
FROM python:3.11-slim

# Evita *.pyc e força stdout/stderr sem buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Pasta de trabalho
WORKDIR /app

# Dependências do sistema (Pillow e redes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ====== Instala Python deps ======
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ====== Copia o projeto ======
COPY . /app/

# ====== Coleta os estáticos ======
# WhiteNoise serve "staticfiles" em produção.
# Se o collectstatic falhar por algum motivo, não quebra o build.
RUN python manage.py collectstatic --noinput || true

# ====== Segurança e rede ======
# Render expõe a app via proxy. Não force redirect aqui no Docker.
ENV PORT=8000
EXPOSE 8000

# ====== Entrada ======
# Executa migrações e sobe o gunicorn na inicialização do container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
