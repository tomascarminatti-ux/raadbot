#!/bin/bash
# scripts/new_run.sh – Crea la estructura de carpetas para una nueva ejecución
#
# Uso:
#   ./scripts/new_run.sh <search_id>
#
# Ejemplo:
#   ./scripts/new_run.sh SEARCH-2026-001

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Error: Debes proporcionar un search_id"
  echo "Uso: ./scripts/new_run.sh <search_id>"
  echo "Ejemplo: ./scripts/new_run.sh SEARCH-2026-001"
  exit 1
fi

SEARCH_ID="$1"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUN_DIR="${BASE_DIR}/runs/${SEARCH_ID}"

if [ -d "$RUN_DIR" ]; then
  echo "Error: Ya existe un run para '${SEARCH_ID}' en ${RUN_DIR}"
  exit 1
fi

mkdir -p "${RUN_DIR}/inputs"
mkdir -p "${RUN_DIR}/outputs"
mkdir -p "${RUN_DIR}/logs"

# Crear archivo de metadata
cat > "${RUN_DIR}/logs/metadata.json" << EOF
{
  "search_id": "${SEARCH_ID}",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "initialized",
  "pipeline_version": "v1.2",
  "candidates": [],
  "notes": ""
}
EOF

# Crear checklist de inputs
cat > "${RUN_DIR}/inputs/README.md" << 'EOF'
# Inputs requeridos

## Para GEM5 (una vez por búsqueda)
- [ ] `brief_jd.txt` – Brief / Job Description
- [ ] `kickoff_notes.txt` – Notas de kick-off
- [ ] `company_context.txt` – Contexto de la compañía

## Por candidato (crear subcarpeta `inputs/<candidate_id>/`)
- [ ] `cv.txt` – CV del candidato
- [ ] `interview_notes.txt` – Notas de entrevista
- [ ] `tests.txt` – Resultados de tests/assessments
- [ ] `case_notes.txt` – Notas de caso/entrevista conductual
- [ ] `references.txt` – Entrevistas con referencias
- [ ] `client_culture.txt` – Descripción de cultura del cliente
EOF

echo "✅ Run creado exitosamente en: ${RUN_DIR}"
echo ""
echo "Estructura:"
echo "  ${RUN_DIR}/"
echo "  ├── inputs/     ← Colocar aquí los inputs (ver README.md)"
echo "  ├── outputs/    ← Se guardarán gemX.json + gemX.md"
echo "  └── logs/       ← Metadata y decisiones"
echo ""
echo "Siguiente paso: agregar inputs en ${RUN_DIR}/inputs/"
