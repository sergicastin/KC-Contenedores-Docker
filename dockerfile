# Etapa de construcción
FROM python:3.8 AS builder

# Configura el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etapa final
FROM python:3.8-slim

# Configura el directorio de trabajo en /app
WORKDIR /app

# Instala la biblioteca de registro json
RUN pip install python-json-logger

# Crea la carpeta logs en el directorio raíz del proyecto con permisos de escritura para todos los usuarios
RUN mkdir /app/logs && chmod 777 /app/logs

# Configura la salida de logs a formato JSON en /logs/app.log
ENV PYTHONJSONLOGGER_LOG_PATH=/app/logs/
ENV PYTHONJSONLOGGER_LOG_FILENAME=app.log
ENV PYTHONJSONLOGGER_JSON_INDENT=4

# Copia solo los archivos necesarios desde la etapa de construcción
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /app /app

# Copia los archivos de la aplicación al contenedor
COPY app /app

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
