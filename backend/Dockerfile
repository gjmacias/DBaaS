
FROM python:3.12-slim

# Evita generar archivos .pyc y fuerza logs inmediatos.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Copiamos primero las dependencias.
COPY requirements.txt .

# 2. Instalamos dependencias en una capa independiente.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 3. Copiamos el código después de instalar dependencias.
COPY app/ ./app/

# 4. Puerto de la API.
EXPOSE 8000

# 5. Arranque de FastAPI.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
