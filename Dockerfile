# Use uma imagem Python 3.10 Slim
FROM python:3.10-slim

# Instala as bibliotecas de sistema necessárias para o Pillow
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Configura o ambiente
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Copia os arquivos de dependência e instala (incluindo Pillow)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . /app/

# Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput

# Comando de execução (Start Command: Gunicorn)
CMD gunicorn core.wsgi
