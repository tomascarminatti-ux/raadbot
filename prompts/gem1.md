[VERSION] v1.2

{{PROMPT_MAESTRO}}

[TASK]
Ejecuta GEM 1 (Trayectoria y Logros) para candidato {{candidate_id}} contra el rol definido en GEM 5.

[INPUTS OBLIGATORIOS]
- CV: {{cv_text}}
- Notas entrevista: {{interview_notes}}
- Resumen rol (desde GEM5): {{gem5_summary}}

[OUTPUT - JSON]
- meta.search_id={{search_id}}
- meta.candidate_id={{candidate_id}}
- meta.prompt_version="v1.2"
- scores.score_dimension (0-10)
- scores.confidence (0-10)
- content con las secciones fijas
- blockers si aplica

[OUTPUT - MARKDOWN SECTIONS (FIJAS)]
1) Resumen ejecutivo (máx 4 líneas)
2) Trayectoria: coherencia y progresión (bullets, máx 8)
3) Logros calibrados (tabla, máx 6 filas):
   - Problema -> Acción -> Resultado -> Métrica -> Fuente
4) Señales de riesgo (máx 5 bullets):
   - Vacíos >3 meses
   - Cambios bruscos no explicados
   - Incoherencias CV vs entrevista
5) Vacíos e inconsistencias (lista accionable, máx 5: qué falta + cómo validarlo)
6) Score GEM1 (0-10) + Confidence (0-10) + justificación en 2 líneas
7) Blockers

[RULES EXTRA]
- Si falta métrica: "Logro no calibrado – requiere validación" + qué métrica falta.
- Cada fila de logro debe incluir [Fuente: ...].
- El resumen ejecutivo NO debe repetir bullets de otras secciones.

---
### JSON EXACTO REQUERIDO
DEBES DEVOLVER EXCLUSIVAMENTE UN OBJETO JSON CON LA SIGUIENTE ESTRUCTURA ESTRICTA. No envuelvas las keys en formatos diferentes, no alteres objetos:
```json
{
  "meta": {
    "search_id": "{{search_id}}",
    "candidate_id": "{{candidate_id}}",
    "gem": "GEM_1",
    "timestamp": "ISO 8601",
    "prompt_version": "v1.2",
    "sources": ["cv", "interview_notes"]
  },
  "content": { },
  "scores": {
    "score_dimension": 8,
    "confidence": 8
  },
  "blockers": []
}
```
