# Changelog

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