#!/bin/bash

# start_localhost.sh - Inicia Raadbot API en localhost:8000

echo "🚀 Iniciando Raadbot API en localhost..."

# Verificar si existe el archivo .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "❗ Por favor, edita el archivo .env y configura tu GEMINI_API_KEY."
fi

# Intentar instalar dependencias si no están (opcional, pero recomendado)
# pip install -r requirements.txt

# Ejecutar la API usando uvicorn
echo "📡 Servidor corriendo en http://localhost:8000"
echo "📖 Swagger UI disponible en http://localhost:8000/docs"
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
