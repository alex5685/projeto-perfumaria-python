# Imagem base
FROM python:3.10-slim

# Variável de ambiente (para evitar buffers)
ENV PYTHONUNBUFFERED 1

# Instala as bibliotecas de sistema necessárias para o Pillow
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Cria o diretório de trabalho
WORKDIR /usr/src/app

# Copia apenas o requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Comando de execução (Start Command)
# Usa a forma mais segura com o binário direto, já que o pip foi bem-sucedido.
CMD ["/usr/local/bin/gunicorn", "core.wsgi"]
