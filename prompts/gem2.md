'{{PROMPT_MAESTRO}}'

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
- scores.score_dimension (0-10)
- scores.confidence (0-10)
- content con secciones fijas
- blockers si aplica

[OUTPUT - MARKDOWN SECTIONS (FIJAS)]
1) Capacidad de ejecución (evidencia conductual)
2) Desempeño bajo presión (2 patrones observables + fuente)
3) Estilo de trabajo (trade-offs, riesgos)
4) Encaje vs desafío crítico (match/mismatch explícito)
5) Tensiones y contradicciones (tests vs entrevista vs caso vs CV)
6) Score GEM2 (0-10) + Confidence (0-10)
7) Blockers

[RULES EXTRA]
- No usar lenguaje psicológico abstracto. Convertir a conducta + impacto.
- Si algo es inferencia: marcar como "Hipótesis no validada – requiere verificación".