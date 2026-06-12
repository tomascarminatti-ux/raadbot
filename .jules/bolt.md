## 2025-05-22 - [Optimización de `build_prompt`]
**Learning:** El uso de múltiples llamadas a `str.replace()` en un bucle sobre un template grande genera muchos objetos string intermedios. Además, la lectura repetida de archivos de prompts desde disco es un cuello de botella innecesario para prompts estáticos.
**Action:** Implementar `functools.lru_cache` para la carga de templates y utilizar `re.sub()` con una función de callback para realizar todos los reemplazos de variables en una sola pasada.
