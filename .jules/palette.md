## 2025-05-15 - [Copy to Clipboard & A11y]
**Learning:** Adding ARIA labels to dynamically generated buttons (like GEM list) is crucial as they lack persistent HTML context for screen readers. Providing immediate visual feedback ("¡Copiado!") after clipboard actions significantly improves perceived system responsiveness.
**Action:** Always include `aria-label` in template literals for dynamic JS rendering and implement transient UI states for confirmation of async/background actions.
