# Raadbot – RAAD GEM Industrial Pipeline

Pipeline secuencial de IA para estandarizar reportes de **búsqueda ejecutiva** en RAAD.

## Qué hace

Convierte datos crudos de candidatos (CV, entrevistas, tests, referencias) en reportes ejecutivos estandarizados con control de calidad automático y trazabilidad de evidencia.

## Pipeline GEM

```
GEM5 (Radiografía Estratégica) → una vez por búsqueda
  ↓
GEM1 (Trayectoria y Logros) → por candidato
  ↓
GEM2 (Assessment a Negocio) → por candidato
  ↓
GEM3 (Veredicto + Referencias 360°) → por candidato
  ↓
GEM4 (Auditor QA – Gate Final) → por candidato
```

### Gating

| GEM | Threshold | Acción si no pasa |
|-----|-----------|-------------------|
| GEM1 → GEM2 | Score ≥ 6 | Candidato descartado |
| GEM2 → GEM3 | Score ≥ 6 | Candidato descartado |
| GEM3 → GEM4 | Score ≥ 6 | Candidato descartado |
| GEM4 → Envío | Score ≥ 7 | BLOQUEO TOTAL (máx 2 reintentos) |

## Quickstart

```bash
# 1. Clonar
git clone <repo-url>
cd raadbot

# 2. Crear una nueva ejecución
./scripts/new_run.sh SEARCH-2026-001

# 3. Colocar inputs en runs/SEARCH-2026-001/inputs/
#    (ver inputs/README.md para checklist)

# 4. Ejecutar cada GEM secuencialmente en tu LLM:
#    - Inyectar prompts/00_prompt_maestro.md + prompts/gemX.md
#    - Reemplazar {{variables}} con datos reales
#    - Guardar outputs en runs/SEARCH-2026-001/outputs/

# 5. Validar output JSON contra el schema
./scripts/validate_output.sh runs/SEARCH-2026-001/outputs/gem1.json
```

## Estructura del proyecto

```
raadbot/
├── CLAUDE.md                      # Reglas del pipeline para el agente
├── prompts/
│   ├── 00_prompt_maestro.md       # Prompt base (rol + reglas + scoring rubric)
│   ├── gem1.md … gem5.md          # Prompt de cada módulo
├── specs/
│   └── gem1…gem5.spec.json        # Contrato de cada módulo
├── schemas/
│   └── gem_output.schema.json     # JSON Schema validable
├── templates/
│   ├── output_example.json        # Ejemplo completo de output GEM1
│   └── variables.md               # Registro de todas las {{variables}}
├── scripts/
│   ├── new_run.sh                 # Crear estructura de ejecución
│   └── validate_output.sh         # Validar output contra schema
└── runs/<search_id>/              # Ejecuciones
    ├── inputs/                    # CV, entrevistas, tests, brief
    ├── outputs/                   # gemX.json + gemX.md
    └── logs/                      # Metadata y decisiones
```

## Reglas clave

- **Evidencia obligatoria**: toda afirmación cita su fuente `[Fuente: ...]`
- **Sin fluff**: prohibido adjetivos vacíos sin métricas
- **Recomendación binaria**: SÍ o NO, sin ambigüedades
- **Post-bloqueo**: máx 2 reintentos, luego escalar a consultor senior
- **Scoring rubric**: definiciones claras de 1-10 en `00_prompt_maestro.md`

## Requisitos

- Acceso a un LLM (Claude, GPT-4, etc.)
- Python 3 + `jsonschema` (para validación): `pip install jsonschema`
- Bash (para scripts)
