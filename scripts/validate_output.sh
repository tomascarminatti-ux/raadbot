#!/bin/bash
# scripts/validate_output.sh – Valida un output JSON contra el schema
#
# Requisitos:
#   pip install jsonschema (o: brew install python-jsonschema)
#
# Uso:
#   ./scripts/validate_output.sh <path_to_output.json>
#
# Ejemplo:
#   ./scripts/validate_output.sh runs/SEARCH-2026-001/outputs/gem1.json

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Error: Debes proporcionar la ruta al archivo JSON a validar"
  echo "Uso: ./scripts/validate_output.sh <path_to_output.json>"
  exit 1
fi

JSON_FILE="$1"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCHEMA_FILE="${BASE_DIR}/schemas/gem_output.schema.json"

if [ ! -f "$JSON_FILE" ]; then
  echo "Error: No se encontró el archivo: ${JSON_FILE}"
  exit 1
fi

if ! command -v python3 &> /dev/null; then
  echo "Error: Se requiere python3"
  exit 1
fi

python3 -c "
import json, sys
try:
    from jsonschema import validate, ValidationError
except ImportError:
    print('Error: Instalar jsonschema -> pip install jsonschema')
    sys.exit(1)

with open('${SCHEMA_FILE}') as f:
    schema = json.load(f)
with open('${JSON_FILE}') as f:
    data = json.load(f)

try:
    validate(instance=data, schema=schema)
    gem = data.get('meta', {}).get('gem', '?')
    score = data.get('scores', {}).get('score_dimension', 'N/A')
    confidence = data.get('scores', {}).get('confidence', 'N/A')
    blockers = len(data.get('blockers', []))
    decision = data.get('decision', '-')
    print(f'✅ Validación exitosa')
    print(f'   GEM: {gem}')
    print(f'   Score: {score} | Confidence: {confidence}')
    print(f'   Blockers: {blockers}')
    if decision != '-':
        print(f'   Decisión: {decision}')
except ValidationError as e:
    print(f'❌ Validación fallida')
    print(f'   Error: {e.message}')
    print(f'   Path: {\" -> \".join(str(p) for p in e.absolute_path)}')
    sys.exit(1)
"
