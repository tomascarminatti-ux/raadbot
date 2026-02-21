[VERSION] v1.2

{{PROMPT_MAESTRO}}

[TASK]
Ejecuta GEM 3 (Veredicto + Referencias 360°) para candidato {{candidate_id}}.

[INPUTS OBLIGATORIOS]
- Output GEM1: {{gem1}}
- Output GEM2: {{gem2}}
- Texto referencias: {{references_text}}
- Cultura cliente: {{client_culture}}

[OUTPUT - JSON]
- meta.search_id={{search_id}}
- meta.candidate_id={{candidate_id}}
- meta.prompt_version="v1.2"
- scores.score_dimension (0-10)
- scores.confidence (0-10)
- content con secciones fijas
- blockers si aplica

[OUTPUT - MARKDOWN SECTIONS (FIJAS)]
1) Encaje estratégico (match explícito: competencias candidato vs requisitos rol GEM5 – tabla 2 columnas, máx 6 filas)
2) Encaje cultural (evidencia conductual vs cultura del cliente – máx 4 bullets)
3) FODA contextualizado (Fortalezas / Oportunidades / Debilidades / Amenazas – máx 3 ítems por cuadrante, cada uno con [Fuente])
4) Riesgos explícitos + variables inciertas (máx 5 bullets con impacto potencial)
5) Referencias: confirma/contradice (tabla: Referente → Rol → Qué confirma → Qué contradice → Fuente)
6) Recomendación binaria: SI / NO (sin ambigüedades ni "podría funcionar")
   - Justificación en máx 3 bullets con evidencia
7) Score GEM3 (0-10) + Confidence (0-10) + justificación en 2 líneas
8) Blockers

[RULES EXTRA]
- La recomendación DEBE ser binaria: SI o NO. Si no hay recomendación binaria => salida inválida.
- No repetir hallazgos de GEM1/GEM2 sin agregar valor nuevo (síntesis, no copia).
- Contrastar explícitamente lo dicho por referencias vs lo observado en entrevistas/tests.
- Si una referencia contradice datos previos: marcar como "Contradicción crítica" + detallar.


---
### JSON EXACTO REQUERIDO
DEBES DEVOLVER EXCLUSIVAMENTE UN OBJETO JSON CON LA SIGUIENTE ESTRUCTURA ESTRICTA. No envuelvas las keys en formatos diferentes, no alteres objetos:
```json
{
  "meta": {
    "search_id": "{{search_id}}",
    "candidate_id": "{{candidate_id}}",
    "gem": "GEM_3",
    "timestamp": "ISO 8601",
    "prompt_version": "v1.2",
    "sources": ["gem1", "gem2", "references", "client_culture"]
  },
  "content": { },
  "scores": {
    "score_dimension": 8,
    "confidence": 8
  },
  "blockers": []
}
```
