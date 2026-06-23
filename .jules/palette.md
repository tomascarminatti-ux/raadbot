## 2025-05-15 - Feedback Visual e Accesibilidad en Dashboard

**Learning:** Proporcionar feedback visual inmediato para acciones asíncronas "invisibles" (como copiar al portapapeles) mejora significativamente la percepción de respuesta del sistema. Además, el uso de estados `focus-visible` y `aria-label` es fundamental para una experiencia de usuario profesional y accesible, especialmente en interfaces densas de datos.

**Action:** Implementar siempre estados de feedback (ej: "¡Copiado!") y asegurar que todos los elementos interactivos tengan etiquetas ARIA descriptivas y estados de foco visibles. Ocultar botones de acción que dependen de una selección previa hasta que dicha selección ocurra para evitar confusión.
