## 2025-05-15 - Optimización de Validación de Esquema y Carga de Prompts
**Learning:** El uso de `jsonschema.validate` recompila el esquema en cada llamada, lo cual es ineficiente en pipelines iterativos. Asimismo, la carga repetitiva de archivos de texto (prompts) desde disco introduce latencia innecesaria.
**Action:** Pre-compilar el validador de esquema (`Draft7Validator`) y usar caché en memoria (`lru_cache`) para archivos estáticos y regex.
