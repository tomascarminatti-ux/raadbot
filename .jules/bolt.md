## 2024-05-23 - Optimización de Prompt Builder
**Learning:** El uso de múltiples llamadas a `.replace()` para la sustitución de variables en templates es ineficiente ((N \times M)$) y la lectura repetida de archivos de templates desde el disco añade una latencia significativa (~0.15-0.2ms por llamada).
**Action:** Implementar `functools.lru_cache` para la carga de templates y utilizar `re.sub()` con un callback para realizar sustituciones en una sola pasada ((N)$), reduciendo la latencia en un orden de magnitud (~13x de mejora).
