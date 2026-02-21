# Variables de Template – Raadbot

Registro centralizado de todas las variables `{{}}` usadas en los prompts.

## Variables globales (todos los GEMs)

| Variable | Tipo | Descripción | Ejemplo |
|----------|------|-------------|---------|
| `{{PROMPT_MAESTRO}}` | string | Contenido completo de `00_prompt_maestro.md` | (inyectado automáticamente) |
| `{{search_id}}` | string | ID único de la búsqueda ejecutiva | `SEARCH-2026-001` |
| `{{candidate_id}}` | string | ID único del candidato | `CAND-001` |

## GEM5 – Radiografía Estratégica

| Variable | Tipo | Obligatorio | Descripción |
|----------|------|:-----------:|-------------|
| `{{jd_text}}` | text | ✅ | Texto completo del Brief / Job Description |
| `{{kickoff_notes}}` | text | ✅ | Notas de la reunión de kick-off con el cliente |
| `{{company_context}}` | text | ⚠️ | Contexto de la compañía (industria, cultura, momento estratégico) |

## GEM1 – Trayectoria y Logros

| Variable | Tipo | Obligatorio | Descripción |
|----------|------|:-----------:|-------------|
| `{{cv_text}}` | text | ✅ | CV completo del candidato (texto plano) |
| `{{interview_notes}}` | text | ✅ | Notas de entrevista estructurada |
| `{{gem5_summary}}` | text | ✅ | Resumen ejecutivo del GEM5 (output previo) |

## GEM2 – Assessment a Negocio

| Variable | Tipo | Obligatorio | Descripción |
|----------|------|:-----------:|-------------|
| `{{gem1}}` | JSON | ✅ | Output completo de GEM1 |
| `{{tests_text}}` | text | ✅ | Resultados de tests / assessments |
| `{{case_notes}}` | text | ✅ | Notas de caso / entrevista conductual |
| `{{gem5_key_challenge}}` | text | ✅ | Desafío crítico del rol (extraído de GEM5) |

## GEM3 – Veredicto + Referencias 360°

| Variable | Tipo | Obligatorio | Descripción |
|----------|------|:-----------:|-------------|
| `{{gem1}}` | JSON | ✅ | Output completo de GEM1 |
| `{{gem2}}` | JSON | ✅ | Output completo de GEM2 |
| `{{references_text}}` | text | ✅ | Texto de entrevistas con referencias |
| `{{client_culture}}` | text | ✅ | Descripción de cultura del cliente |

## GEM4 – Auditor QA

| Variable | Tipo | Obligatorio | Descripción |
|----------|------|:-----------:|-------------|
| `{{gem1}}` | JSON | ✅ | Output completo de GEM1 |
| `{{gem2}}` | JSON | ✅ | Output completo de GEM2 |
| `{{gem3}}` | JSON | ✅ | Output completo de GEM3 |
| `{{sources_index}}` | text | ✅ | Índice de todas las fuentes disponibles |

## Notas
- `✅` = Input obligatorio. Si falta, el GEM debe declarar blocker.
- `⚠️` = Input recomendado. Si falta, baja el confidence score.
- `{{gem5_summary}}` y `{{gem5_key_challenge}}` se extraen del output de GEM5 pero son secciones distintas.
