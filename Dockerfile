# Imagem base (que resolveu o Pillow)
FROM python:3.10-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Instala as libs de sistema (Pillow)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copia e instala (O Render vai gerenciar o venv, mas isso garante que as dependências estejam lá)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . /app/

# Remove o CMD para forçar o Render a usar o Start Command da UI.
# REMOVA A LINHA CMD.
