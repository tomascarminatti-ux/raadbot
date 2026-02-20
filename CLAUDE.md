# RAAD GEM Industrial Pipeline (v1)

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
1) outputs/gemX.json (machine-readable)
2) outputs/gemX.md   (human-readable)

## Umbrales de gating
- GEM1 >= 6 para continuar a GEM2
- GEM2 >= 6 para continuar a GEM3
- GEM3 >= 6 para continuar a GEM4
- GEM4 >= 7 para aprobar entrega

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