# 1. IMAGEM BASE: A imagem slim é a melhor para produção.
FROM python:3.10-slim

# 2. VARIÁVEIS DE AMBIENTE: Desativa o buffer para logs em tempo real.
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# 3. INSTALAÇÃO DE LIBS DE SISTEMA (SOLUÇÃO FINAL PARA O PILLOW - ERRNO 2)
# O apt-get instala as dependências de sistema para compilar o Pillow (libjpeg, zlib).
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# 4. INSTALAÇÃO DE DEPENDÊNCIAS PYTHON
# Copia e instala as dependências do requirements.txt (incluindo Django e Gunicorn).
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. CÓPIA DO CÓDIGO DO PROJETO
# Copia todos os arquivos restantes (settings.py, core, apps, etc.).
COPY . /app/

# 6. COLETA DE ARQUIVOS ESTÁTICOS
# Roda o collectstatic, que é necessário antes do app iniciar.
# Como ele é RUN, ele ocorre durante o processo de build do Docker.
RUN python manage.py collectstatic --noinput

# 6A. EXECUÇÃO DAS MIGRAÇÕES (!!! ESSA É A NOVA LINHA !!!)
RUN python manage.py migrate

# 7. COMANDO DE EXECUÇÃO (START/CMD)
# O CMD mais portátil: executa o Gunicorn como um módulo Python (python -m),
# ignorando problemas de PATH (Status 127).
CMD ["python", "-m", "gunicorn", "core.wsgi"]

