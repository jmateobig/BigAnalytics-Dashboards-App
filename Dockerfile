# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia los requerimientos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto
COPY . .

# Establece las variables de entorno (opcional si usas .env en docker-compose)
ENV PYTHONUNBUFFERED=1

# Expone el puerto que usarás (8000)
EXPOSE 8000

# Usa Gunicorn como servidor de producción
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "publication.wsgi:application"]
