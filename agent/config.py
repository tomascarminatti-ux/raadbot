"""
config.py – Configuración centralizada para el pipeline.
"""

import os

# Thresholds de gating
THRESHOLDS = {
    "gem1": 6,
    "gem2": 6,
    "gem3": 6,
    "gem4": 7,
}

# Reintentos de validación de schema
MAX_RETRIES_ON_BLOCK = 2

# Costos Gemini 2.0 Flash (por 1M tokens) - Ajustar según precios vigentes
PRICE_PROMPT_1M = 0.075
PRICE_COMPLETION_1M = 0.30

# Modelo por defecto - Cambiado a gemini-2.0-flash (v2.5 no existe)
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
