## 2025-05-22 - [Optimización de construcción de prompts y carga de schemas]
**Learning:** Eliminar E/S de disco redundante y reemplazos iterativos de cadenas en la construcción de prompts y validación de schemas proporciona mejoras de velocidad de orden de magnitud en pipelines intensivos de LLM.
**Action:** Usar siempre `lru_cache` para archivos estáticos como templates de prompts y schemas de validación. Implementar inyección de variables en templates usando `re.sub` con un callback en lugar de múltiples llamadas a `.replace()`.
