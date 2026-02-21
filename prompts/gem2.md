[VERSION] v1.2

{{PROMPT_MAESTRO}}

[TASK]
Ejecuta GEM 2 (Assessment a negocio) para {{candidate_id}}.

[INPUTS OBLIGATORIOS]
- Output GEM1: {{gem1}}
- Tests / assessment: {{tests_text}}
- Caso / entrevista conductual: {{case_notes}}
- Desafío crítico del rol (GEM5): {{gem5_key_challenge}}

[OUTPUT - JSON]
- meta.search_id={{search_id}}
- meta.candidate_id={{candidate_id}}
- meta.prompt_version="v1.2"
- scores.score_dimension (0-10)
- scores.confidence (0-10)
- content con secciones fijas
- blockers si aplica

[OUTPUT - MARKDOWN SECTIONS (FIJAS)]
1) Capacidad de ejecución (evidencia conductual, máx 4 bullets)
2) Desempeño bajo presión (2 patrones observables + fuente)
3) Estilo de trabajo (trade-offs, riesgos – máx 4 bullets)
4) Encaje vs desafío crítico (match/mismatch explícito – tabla 2 columnas: requisito → evidencia)
5) Tensiones y contradicciones (tests vs entrevista vs caso vs CV – máx 4 bullets)
6) Score GEM2 (0-10) + Confidence (0-10) + justificación en 2 líneas
7) Blockers

[RULES EXTRA]
- No usar lenguaje psicológico abstracto. Convertir a conducta + impacto.
- Si algo es inferencia: marcar como "Hipótesis no validada – requiere verificación".
- No repetir hallazgos de GEM1 sin agregar valor nuevo (análisis, no copia).

---
### JSON EXACTO REQUERIDO
DEBES DEVOLVER EXCLUSIVAMENTE UN OBJETO JSON CON LA SIGUIENTE ESTRUCTURA ESTRICTA. No envuelvas las keys en formatos diferentes, no alteres objetos:
```json
{
  "meta": {
    "search_id": "{{search_id}}",
    "candidate_id": "{{candidate_id}}",
    "gem": "GEM_2",
    "timestamp": "ISO 8601",
    "prompt_version": "v1.2",
    "sources": ["gem1", "tests", "case_notes"]
  },
  "content": { },
  "scores": {
    "score_dimension": 8,
    "confidence": 8
  },
  "blockers": []
}
```
