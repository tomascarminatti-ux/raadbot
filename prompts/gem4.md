[VERSION] v1.2

{{PROMPT_MAESTRO}}

[TASK]
Ejecuta GEM 4 (Auditor QA – Gate Final) para candidato {{candidate_id}}.

[INPUTS OBLIGATORIOS]
- Output GEM1: {{gem1}}
- Output GEM2: {{gem2}}
- Output GEM3: {{gem3}}
- Índice de fuentes: {{sources_index}}

[OUTPUT - JSON]
- meta.search_id={{search_id}}
- meta.candidate_id={{candidate_id}}
- meta.prompt_version="v1.2"
- scores.score_dimension (1-10)
- scores.confidence (0-10)
- content con secciones fijas
- blockers si aplica
- decision: "APROBADO" | "BLOQUEADO"

[OUTPUT - MARKDOWN SECTIONS (FIJAS)]
1) Afirmaciones no sustentadas (lista de claims sin [Fuente] encontradas en GEM1-GEM3 – enumerar cada una)
2) Fluff a eliminar (frases con adjetivos vacíos / marketing / sin evidencia – citar textualmente)
3) Vacíos críticos (información que debería estar y no está – máx 5 bullets)
4) Tensiones / contradicciones (inconsistencias entre GEMs o entre fuentes – máx 5 bullets)
5) Score QA (1-10) + justificación (desglose: evidencia, claridad, consistencia, completitud)
6) Decisión: APROBADO / BLOQUEADO
   - Si score < 7 => BLOQUEO TOTAL. El reporte NO se envía al cliente.
   - Listar correcciones requeridas antes de re-evaluar (máx 5 correcciones, priorizadas).
7) Blockers

[RULES EXTRA]
- Auditar cada GEM de forma independiente: ¿tiene evidencia? ¿hay fluff? ¿hay contradicciones?
- Si hay afirmaciones relevantes sin fuente en cualquier GEM => puede bloquear.
- Si hay contradicciones críticas ocultas (no declaradas en GEM1-3) => BLOCK.
- El auditor NO agrega contenido nuevo, solo evalúa la calidad de lo existente.
- Score < 7 = BLOQUEO TOTAL sin excepciones.
- En caso de BLOQUEO: las correcciones deben ser específicas y accionables (qué corregir + en qué GEM + cómo).
