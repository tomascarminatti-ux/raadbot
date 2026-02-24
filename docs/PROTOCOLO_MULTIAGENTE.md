# Protocolo Operativo Multiagente (GEM1–GEM5 + Supervisor General)

## 1) Objetivo
Estandarizar la evaluación ejecutiva con un sistema de 5 agentes especialistas (GEM) y un **Supervisor General** que gobierna calidad, consistencia, trazabilidad y escalamiento.

Este protocolo define:
- responsabilidades por agente,
- contratos mínimos de entrada/salida,
- reglas de gating (avance/descartes),
- reintentos y escalamiento,
- criterios de auditoría y publicación final.

---

## 2) Roles del sistema

### GEM5 — Radiografía Estratégica (Hito 0)
**Propósito:** traducir JD + kick-off + contexto compañía a una hipótesis de mandato accionable.

**Entradas mínimas:**
- `jd_text`
- `kickoff_notes`
- `company_context`

**Salida esperada:**
- problema real del rol,
- éxitos esperados (12–18 meses, con KPI),
- no-fits,
- stakeholders y tensiones,
- mapa de mercado,
- riesgos del mandato,
- criterios de decisión final.

**Gate:** no usa score de candidato (`score_dimension = null`), pero sí `confidence` y `blockers`.

**Regla crítica:** si faltan JD o kickoff, **BLOCK** inmediato.

---

### GEM1 — Trayectoria y Logros
**Propósito:** validar coherencia de carrera, evidencia de resultados y calidad de logros.

**Entradas mínimas:**
- `cv_text`
- `interview_notes`
- resumen de GEM5 (`gem5_summary`)

**Salida esperada:**
- trayectoria y progresión,
- logros calibrados (Problema → Acción → Resultado → Métrica → Fuente),
- riesgos de continuidad y coherencia,
- vacíos de evidencia.

**Gate de avance:** `score_dimension >= 6`.

**Si falla gate:** `DESCARTADO_GEM1`.

---

### GEM2 — Assessment a Negocio
**Propósito:** medir capacidad real de ejecución frente al desafío del mandato.

**Entradas mínimas:**
- output de GEM1,
- `tests_text`,
- `case_notes`,
- desafío crítico de GEM5 (`gem5_key_challenge`).

**Salida esperada:**
- capacidad de ejecución,
- desempeño bajo presión,
- estilo de trabajo y trade-offs,
- encaje explícito vs desafío crítico,
- contradicciones entre CV/test/caso/entrevista.

**Gate de avance:** `score_dimension >= 6`.

**Si falla gate:** `DESCARTADO_GEM2`.

---

### GEM3 — Veredicto + Referencias 360
**Propósito:** consolidar encaje estratégico/cultural y emitir recomendación binaria.

**Entradas mínimas:**
- outputs GEM1 y GEM2,
- `references_text`,
- `client_culture`.

**Salida esperada:**
- encaje estratégico,
- encaje cultural,
- FODA contextualizado,
- riesgos explícitos,
- matriz de referencias (confirma/contradice),
- recomendación **SI/NO** sin ambigüedad.

**Gate de avance:** `score_dimension >= 6`.

**Si falla gate:** `DESCARTADO_GEM3`.

---

### GEM4 — Auditor QA (Gate Final)
**Propósito:** auditar calidad transversal (evidencia, consistencia, anti-fluff, vacíos).

**Entradas mínimas:**
- outputs GEM1–GEM3,
- índice de fuentes (`sources_index`).

**Salida esperada:**
- claims sin sustento,
- frases de fluff a eliminar,
- vacíos críticos,
- contradicciones entre GEMs/fuentes,
- score QA + decisión final.

**Gate final:**
- `score_dimension >= 7` **y** `decision != BLOQUEADO` → APROBADO.
- `score_dimension < 7` → BLOQUEO TOTAL.

**Reintentos:** máximo 2 iteraciones de corrección/auditoría.

**Si no supera reintentos:** escalamiento humano.

---

## 3) Supervisor General (orquestador + gobernanza)

### Misión
El Supervisor General coordina a los 5 GEM como un sistema único.

**Prompt de referencia:** `prompts/supervisor_general.md`

El Supervisor General:
1. **Orquesta secuencia y estado:** GEM5 → GEM1 → GEM2 → GEM3 → GEM4.
2. **Aplica gating duro:** no se salta etapas ni umbrales.
3. **Administra reintentos:** hasta 2 en bloqueo QA.
4. **Garantiza compliance:** evidencia obligatoria, no invención, no relleno de vacíos.
5. **Define salida operativa:** APROBADO, DESCARTADO por etapa o ESCALADO.

### Responsabilidades concretas
- Validar que inputs críticos existan antes de ejecutar cada GEM.
- Asegurar contrato JSON mínimo en cada salida.
- Verificar consistencia inter-GEM (no contradicción no declarada).
- Exigir declaración explícita de incertidumbre: `No informado en fuentes` o `Hipótesis no validada`.
- Trazar costos/tokens y estado para reanudación.

### Decisiones permitidas del supervisor
- `DESCARTADO_GEM1`, `DESCARTADO_GEM2`, `DESCARTADO_GEM3`
- `BLOQUEADO_QA_REINTENTO`
- `APROBADO`
- `ESCALADO_CONSULTOR_SENIOR`

---

## 4) Reglas no negociables (transversales)
1. Cero invención de datos.
2. Cero frases genéricas sin evidencia.
3. Toda afirmación relevante debe tener fuente.
4. Contradicciones se reportan; no se ocultan.
5. Recomendación de GEM3 obligatoriamente binaria (SI/NO).
6. QA final mínimo 7/10 para liberar reporte.

---

## 5) Protocolo de flujo (estado)

### Pipeline macro
1. **Entrada:** carga de datos (Drive/carpeta local).
2. **GEM5:** radiografía estratégica única por búsqueda.
3. **Iteración por candidato:** GEM1 → GEM2 → GEM3.
4. **Auditoría QA:** GEM4.
5. **Salida:** reporte final (JSON + Markdown) o descarte/escalado.

### Lógica de decisión
- Si GEM1 < 6 → descarte.
- Si GEM2 < 6 → descarte.
- Si GEM3 < 6 → descarte.
- Si GEM4 < 7 o `decision=BLOQUEADO` → bloqueo y reintento (hasta 2).
- Si reintentos agotados y GEM4 sigue bloqueado → `ESCALADO_CONSULTOR_SENIOR`.
- Si GEM4 ≥ 7 y sin bloqueo → reporte final aprobado (`APROBADO`).

---

## 6) Contrato mínimo de interoperabilidad
Todos los agentes deben retornar:
- `meta` (search_id, candidate_id, gem, timestamp, prompt_version, sources),
- `content` (hallazgos del GEM),
- `scores` (`score_dimension`, `confidence`),
- lista de hallazgos críticos/`issues_found` o `blockers`.

> Nota: en GEM5, `score_dimension` puede ser `null` por ser módulo de contexto, no de evaluación de candidato.

---

## 7) Métricas operativas del protocolo
- **Calidad:** tasa de aprobaciones QA ≥ 7.
- **Confiabilidad:** % de salidas con citas completas.
- **Consistencia:** % de contradicciones correctamente declaradas.
- **Eficiencia:** tiempo por candidato y costo total por búsqueda.
- **Escalamiento:** tasa de casos que requieren consultor senior.

---

## 8) Política de escalamiento humano
Escalar automáticamente cuando ocurra cualquiera:
- 3 bloqueos QA consecutivos,
- contradicción crítica irresoluble entre fuentes,
- falta estructural de evidencia para recomendación final,
- ambigüedad persistente en recomendación binaria.

La escalación debe incluir:
- resumen ejecutivo del caso,
- lista de bloqueos/correcciones intentadas,
- riesgos de decisión si se fuerza cierre sin evidencia adicional.

## 9) Estado runtime implementado
El pipeline actual implementa el protocolo con los siguientes comportamientos operativos:
- Gating duro: GEM1/GEM2/GEM3 con umbral `>=6`; GEM4 con umbral `>=7`.
- Reintentos de GEM4: hasta 2 reintentos adicionales cuando QA bloquea (total de 3 intentos).
- Persistencia por intento: `gem4`, `gem4_retry_1`, `gem4_retry_2` en outputs por candidato.
- Decisión final automática:
  - `APROBADO` si GEM4 pasa gate y no está bloqueado.
  - `ESCALADO_CONSULTOR_SENIOR` si GEM4 no logra aprobar tras reintentos.

