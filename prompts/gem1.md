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
- scores.score_dimension (0-10)
- scores.confidence (0-10)
- content con las secciones fijas
- blockers si aplica

[OUTPUT - MARKDOWN SECTIONS (FIJAS)]
1) Resumen ejecutivo (máx 4 líneas)
2) Trayectoria: coherencia y progresión (bullets)
3) Logros calibrados (tabla):
   - Problema -> Acción -> Resultado -> Métrica -> Fuente
4) Señales de riesgo:
   - Vacíos >3 meses
   - Cambios bruscos no explicados
   - Incoherencias CV vs entrevista
5) Vacíos e inconsistencias (lista accionable: qué falta + cómo validarlo)
6) Score GEM1 (0-10) + Confidence (0-10)
7) Blockers

[RULES EXTRA]
- Si falta métrica: "Logro no calibrado – requiere validación" + qué métrica falta.
- Cada fila de logro debe incluir [Fuente: ...].