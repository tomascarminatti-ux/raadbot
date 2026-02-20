FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del SO si fuese necesario
# RUN apt-get update && apt-get install -y gcc

# Copiar requirements primero para aprovechar el caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto de FastAPI
EXPOSE 8000

# Ejecutar Uvicorn interrumpiendo elegantemente
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
