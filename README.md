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

## Quickstart: Ejecutar el Pipeline

Ahora Raadbot es un **Agente ejecutable** impulsado por Gemini API y Google Drive.

```bash
# 1. Clonar e instalar
git clone https://github.com/tomascarminatti-ux/raadbot.git
cd raadbot
pip install -r requirements.txt

# 2. Configurar credenciales
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY
# (Opcional, para Drive): descargar credentials.json de Google Cloud Console y ponerlo en la raíz

# 3. Crear una nueva ejecución (estructura de carpetas)
./scripts/new_run.sh SEARCH-2026-001

# 4. Colocar inputs
# A) Si usas Google Drive: organiza tus archivos en una carpeta (ver inputs/README.md)
# B) Si usas archivos locales: ponlos en runs/SEARCH-2026-001/inputs/

# 5. Ejecutar el Agente!
# Opcion A: Con Google Drive
python run.py --search-id SEARCH-2026-001 --drive-folder <ID_DE_CARPETA_DRIVE>

# Opcion B: Con archivos locales
python run.py --search-id SEARCH-2026-001 --local-dir runs/SEARCH-2026-001/inputs
```

El agente ejecutará secuencialmente GEM5 → GEM1 → GEM2 → GEM3 → GEM4, aplicando el control de calidad, reintentando si hay bloqueos, y guardando los resultados JSON y Markdown en `runs/SEARCH-2026-001/outputs/`.

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
