[VERSION] v1.2

{{PROMPT_MAESTRO}}

[TASK]
Construye GEM 5 (Radiografía estratégica) para la búsqueda: {{search_id}}.

[INPUTS OBLIGATORIOS]
- Brief/JD: {{jd_text}}
- Notas kick-off: {{kickoff_notes}}
- Contexto compañía: {{company_context}}

[OUTPUT - JSON]
- meta.search_id={{search_id}}
- meta.candidate_id=null
- meta.prompt_version="v1.2"
- content debe incluir TODAS las secciones de abajo.

[OUTPUT - MARKDOWN SECTIONS (FIJAS)]
1) Problema real del rol (3 bullets, máx 2 líneas c/u)
2) Éxitos esperados 12–18 meses (5 bullets medibles con KPI)
3) No-fits (3 bullets con justificación)
4) Stakeholders críticos + tensiones (4 bullets: nombre/rol + tensión)
5) Mapa de mercado (tabla: targets / no-go / competidores – máx 10 filas)
6) Riesgos del mandato (operacionales, políticos, reputacionales – máx 6 bullets)
7) Criterios de decisión final (top 6, ordenados por peso)

[SCORING]
- score_dimension = null (GEM5 no evalúa candidatos)
- confidence (0-10) según completitud de inputs
- blockers si faltan inputs críticos (JD o kickoff)

[RULES EXTRA]
- Si falta brief_jd o kickoff_notes => BLOCK. No ejecutar sin estos inputs.
- Cada sección debe ser accionable: que un consultor pueda usarla para filtrar candidatos.

---
### JSON EXACTO REQUERIDO
DEBES DEVOLVER EXCLUSIVAMENTE UN OBJETO JSON CON LA SIGUIENTE ESTRUCTURA ESTRICTA. No envuelvas las keys en formatos diferentes, no alteres objetos:
```json
{
  "meta": {
    "search_id": "{{search_id}}",
    "candidate_id": null,
    "gem": "GEM_5",
    "timestamp": "ISO 8601",
    "prompt_version": "v1.2",
    "sources": ["brief_jd", "kickoff_notes", "company_context"]
  },
  "content": { },
  "scores": {
    "score_dimension": null,
    "confidence": 8
  },
  "blockers": []
}
```
