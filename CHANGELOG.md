# Changelog

## [v3.0.0] - Industrial Multi-Agent (Hub-and-Spoke 3.0)
### Added
- **GEM 6 Orchestrator**: Nuevo cerebro central autónomo con bucle Thought-Action-Observation.
- **Arquitectura Dinámica**: Transición de pipeline secuencial a modelo Hub-and-Spoke 3.0.
- **Integración con n8n**: Soporte nativo para webhooks asíncronos y triggers externos.
- **Validación de Contratos**: Sistema de validación estricta via JSON Schema entre agentes.
- **GEM 5 Strategy**: Nuevo agente especializado en radiografía de proyectos y mandatos.

### Improved
- **Documentación Industrial**: README totalmente renovado con diagramas Mermaid detallados.
- **Trazabilidad Total**: Implementación de Trace IDs para auditar cada paso del razonamiento.
- **Control de Costos**: Lógica de Early Exit mejorada basada en scoring de GEM 2.

## [v1.5.0] - Arch Architecture Cleanup & Production Ready
### Added
- **Configuración Centralizada**: Creado `config.py` para manejar umbrales, precios, modelos y rutas de forma global.
- **Type Safety**: Implementación de `TypedDict` y mejores hints de tipos en todo el núcleo (`GeminiClient`, `Pipeline`).
- **Resiliencia de Ingesta**: El cargador de inputs ahora es más tolerante a errores de lectura y mejora el matching de archivos.
- **Logging Profesional**: Migración total a `rich.console` para una experiencia CLI premium.

### Improved
- **GeminiClient Robustness**: Regex mejorada para extracción de JSON y manejo de casos donde el LLM no usa etiquetas Markdown.
- **DriveClient Stability**: Mejor manejo de archivos binarios y re-autenticación de tokens.
- **API v1.1**: Soporte para timeouts extendidos en webhooks y mejor reporte de errores en tareas de fondo.

### Fixed
- **Redundancia**: Eliminación de scripts obsoletos (`fix.py`) y limpieza de importaciones duplicadas.
- **Consistency**: Corregido typo persistente en el nombre del modelo (`gemini-2.5` -> `gemini-2.0`).

## [v1.4.1] - Psycho Level Audit & Robustness
### Added
- **Test Suite de Robustez**: Suite de pruebas unitarias (`tests/test_robustness.py`) para verificar el parseo de JSON y normalización de GEMs.
- **Normalización de GEMs**: El pipeline ahora reconcilia automáticamente nombres como `GEM1`, `GEM_1` o `gem-1` para máxima interoperabilidad con prompts personalizados.
- **Limpieza de JSON "Psicópata"**: El cliente de Gemini ahora limpia automáticamente errores comunes como comas finales (trailing commas) antes de parsear, previniendo fallos críticos.
- **Tracking de Finish Reason**: Se captura el motivo de finalización de la API (ej: `MAX_TOKENS`, `STOP`) para mejor diagnóstico.

### Fixed
- **Imports en test_gemini.py**: Se corrigió el problema de rutas para que los tests básicos funcionen desde cualquier contexto.
- **Integridad de Estado**: Mejor manejo de errores al cargar archivos de checkpoint corruptos.


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