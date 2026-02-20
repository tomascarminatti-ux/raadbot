# RAAD GEM Industrial Pipeline (v1.2)

## Objetivo
Estandarizar reportes de búsqueda ejecutiva con un pipeline secuencial GEM:
GEM5 -> GEM1 -> GEM2 -> GEM3 -> GEM4(QA) -> Envío/Bloqueo.

## No negociables
- Pipeline secuencial: no se reordena.
- Evidencia obligatoria: toda afirmación relevante debe tener fuente.
- Si falta evidencia: "No informado en fuentes" o "Hipótesis no validada – requiere verificación".
- Prohibido fluff (adjetivos vacíos).
- Recomendación final binaria: SI / NO (sin "podría funcionar").
- QA Gate: si GEM4 score < 7 => BLOQUEO TOTAL (no se envía).

## Contrato de salida (por GEM)
Cada GEM entrega dos outputs:
1) outputs/gemX.json (machine-readable) – ver `templates/output_example.json` como referencia
2) outputs/gemX.md   (human-readable)

## Umbrales de gating
- GEM1 >= 6 para continuar a GEM2
- GEM2 >= 6 para continuar a GEM3
- GEM3 >= 6 para continuar a GEM4
- GEM4 >= 7 para aprobar entrega

## Rúbrica de scoring (score_dimension)
- **1-2**: Candidato no viable. Brechas fundamentales o evidencia insuficiente.
- **3-4**: Debilidades significativas. Riesgos altos no mitigables.
- **5**: Borderline. Cumple mínimos pero sin diferenciación clara.
- **6-7**: Competente con reservas. Match adecuado con flags menores.
- **8-9**: Fuerte match. Evidencia sólida, riesgos bajos y manejables.
- **10**: Excepcional. Supera requisitos con evidencia contundente.

## Criterio de confidence
El confidence score (0-10) se basa en 3 factores:
- **Completitud de inputs** (¿se recibieron todos los insumos requeridos?)
- **Calidad de evidencia** (¿las fuentes son específicas, recientes, verificables?)
- **Consistencia entre fuentes** (¿coinciden CV, entrevista, tests, referencias?)

Guía:
- **1-3**: Inputs incompletos o contradictorios. Alta incertidumbre.
- **4-6**: Inputs parciales. Algunas inferencias necesarias.
- **7-8**: Inputs completos. Evidencia mayormente consistente.
- **9-10**: Inputs completos + cross-validados. Alta certeza.

## Formato de citación (obligatorio)
Usar uno de estos:
- [Fuente: CV – sección X]
- [Fuente: Entrevista – línea X o minuto Y]
- [Fuente: Test – página Z]
- [Fuente: Caso – observación #]
- [Fuente: Referencia – nombre/rol + fecha]
- [Fuente: Medios – medio + fecha + enlace]

## Idioma y tono
- Español
- Ejecutivo, analítico, sobrio, directo.
- Frases cortas. Bullets. Sin marketing.

## Reglas de inferencia
- Se permite inferir SOLO si:
  1) se explicita como inferencia, y
  2) se listan las evidencias que la sostienen.
Formato: "Hipótesis no validada – requiere verificación: ..."

## Convención de carpetas de ejecución
runs/<search_id>/
  inputs/   (CV, entrevistas, tests, referencias, brief)
  outputs/  (gem5..gem4.json + gem5..gem4.md)
  logs/     (notas, decisiones, cambios)

Usar `scripts/new_run.sh <search_id>` para crear la estructura automáticamente.

## Orquestación del pipeline
1. Cargar `prompts/00_prompt_maestro.md` como contexto base (inyectarlo via `{{PROMPT_MAESTRO}}`).
2. Ejecutar GEM5 con `prompts/gem5.md` + inputs de la búsqueda.
3. Para cada candidato, ejecutar secuencialmente:
   - GEM1 (`prompts/gem1.md`) → verificar score ≥ 6 → si no, detener.
   - GEM2 (`prompts/gem2.md`) → verificar score ≥ 6 → si no, detener.
   - GEM3 (`prompts/gem3.md`) → verificar score ≥ 6 → si no, detener.
   - GEM4 (`prompts/gem4.md`) → verificar score ≥ 7 → si < 7, BLOQUEO TOTAL.
4. Guardar cada output en `runs/<search_id>/outputs/` como `gemX.json` + `gemX.md`.
5. Si GEM4 aprueba, el reporte está listo para envío al cliente.

## Flujo post-bloqueo (ON BLOCK)
Si GEM4 bloquea el reporte (score < 7):

1. **Leer la lista de correcciones requeridas** del output de GEM4.
2. **Identificar el GEM afectado**: las correcciones indicarán en qué GEM(s) está el problema.
3. **Re-ejecutar desde el GEM afectado**, no desde cero:
   - Si el problema es de evidencia en GEM1 → re-ejecutar GEM1 con inputs corregidos/ampliados.
   - Si es un problema de GEM3 → re-ejecutar GEM3 (GEM1 y GEM2 se mantienen si no fueron señalados).
4. **Re-ejecutar GEM4** una vez corregidos los GEM(s) afectados.
5. **Máximo 2 intentos de corrección**. Si tras 2 re-runs GEM4 sigue bloqueando:
   - Escalar al consultor senior para revisión manual.
   - Registrar en `logs/` la decisión y las razones del bloqueo persistente.
6. **Registrar cada intento** en `runs/<search_id>/logs/` con timestamp y cambios realizados.

## Versionamiento de prompts
- Cada ejecución debe registrar en `meta.prompt_version` la versión del prompt utilizada.
- Formato: `v<major>.<minor>` (ej: `v1.2`).
- Al modificar un prompt, incrementar la versión y documentar en `CHANGELOG.md`.
- Ver `templates/variables.md` para la lista completa de variables de template.