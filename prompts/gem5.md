{{PROMPT_MAESTRO}}

[TASK]
Construye GEM 5 (Radiografía estratégica) para la búsqueda: {{search_id}}.

[INPUTS]
- Brief/JD: {{jd_text}}
- Notas kick-off: {{kickoff_notes}}
- Contexto compañía: {{company_context}}

[OUTPUT - JSON]
- meta.search_id={{search_id}}
- meta.candidate_id=null
- content debe incluir TODAS las secciones de abajo.

[OUTPUT - MARKDOWN SECTIONS (FIJAS)]
1) Problema real del rol (3 bullets)
2) Éxitos esperados 12–18 meses (5 bullets medibles)
3) No-fits (3 bullets)
4) Stakeholders críticos + tensiones (4 bullets)
5) Mapa de mercado (targets / no-go / competidores)
6) Riesgos del mandato (operacionales, políticos, reputacionales)
7) Criterios de decisión final (top 6)

[SCORING]
- score_dimension = null
- confidence (0-10) según completitud de inputs
- blockers si faltan inputs críticos (JD o kickoff)