# Changelog

## [v1.5.0] - Async & Architecture Upgrades
### Added
- **Async Pipeline**: Soporte para ejecución asíncrona usando `asyncio` y la API asíncrona de Gemini.
- **Parallel Processing**: Procesamiento de múltiples candidatos en paralelo, acelerando significativamente las ejecuciones con muchos candidatos.
- **Improved Architecture**: Desacoplamiento de lógica, configuración y utilidades.
- **Unit Testing**: Suite de pruebas con `pytest` para Pipeline y API.
- **FastAPI Webhooks**: Soporte para webhooks asíncronos en la API.

### Fixed
- **Invalid Model**: Corregido el nombre del modelo a `gemini-2.0-flash`.
- **Imports Smells**: Eliminados hacks de `sys.path` y dependencias circulares.

## [v1.4.0] - Psycho Level Agent Upgrades
### Added
- **Rich Console UI**: Interfaz de terminal profesional, con spinners de carga, paneles dinámicos y tablas resumen a color.
- **State Checkpointing**: El pipeline ahora guarda su estado localmente (`pipeline_state.json`) permitiendo continuar la ejecución donde se quedó si ocurre un error o se interrumpe (Hot-Reloading).
- **Token & Cost Tracking**: Extracción de metadatos de uso desde la API de Gemini, sumando prompts/completion tokens y calculando el costo total estimado en USD por corrida.
- **Error Handling Avanzado**: Robustecido para tolerar respuestas estructuradas sin etiquetas Markdown correctas.


## v1.3.0
- **Sistema Agente Ejecutable**: Raadbot ahora es un pipeline automatizado.
- Creado `agent/gemini_client.py` usando `google-genai` SDK con retries y parsing de JSON.
- Creado `agent/drive_client.py` con integración a Google Drive API para ingesta de inputs.
- Creado `agent/pipeline.py` para orquestación completa (gating, reintentos post-bloqueo, schema validation).
- Creado `agent/prompt_builder.py` para inyección automática de variables.
- Creado `run.py` como CLI principal (`python run.py --search-id ...`).
- Agregados `requirements.txt` y `.env.example`.

## v1.2.0
- Agregada rúbrica de scoring detallada (1-10) en `00_prompt_maestro.md`.
- Agregado criterio de confidence (completitud × calidad × consistencia).
- Agregado flujo post-bloqueo en `CLAUDE.md` (máx 2 reintentos + escalación).
- Agregado `[VERSION] v1.2` a todos los prompts.
- Agregado `meta.prompt_version` al output JSON de cada prompt.
- Agregados límites de longitud por sección en todos los prompts.
- Creado `schemas/gem_output.schema.json` – JSON Schema validable para outputs.
- Creado `templates/output_example.json` – ejemplo completo de output GEM1.
- Creado `templates/variables.md` – registro centralizado de variables de template.
- Creado `scripts/new_run.sh` – crea estructura de carpetas para nuevas ejecuciones.
- Creado `scripts/validate_output.sh` – valida outputs JSON contra el schema.
- Mejorado `README.md` con quickstart, estructura completa y requisitos.
- Eliminada redundancia entre `CLAUDE.md` y `00_prompt_maestro.md`.

## v1.1.0
- Agregados prompts faltantes: `gem3.md` (Veredicto + Referencias 360°) y `gem4.md` (Auditor QA).
- Corregida sintaxis de template en `gem2.md` (comillas sobrantes en `{{PROMPT_MAESTRO}}`).
- Estandarizado formato JSON en todos los specs (`gem1`, `gem3`, `gem5`).
- Mejorado `README.md` con documentación del pipeline.
- Agregada sección de orquestación y versionamiento de prompts en `CLAUDE.md`.

## v1.0.0
- Versión inicial del pipeline RAAD GEM Industrial.
- Incluye configuración completa (`CLAUDE.md`), reglas persistentes, comandos, especificaciones de agentes, plantillas de prompts y estructura de ejecuciones.