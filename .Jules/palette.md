## 2026-02-21 - Consistent CLI UX Pattern
**Learning:** In backend-heavy tools like this pipeline, the "UI" is the CLI. When core modules (like agent/pipeline.py) use rich formatting but the entry point (run.py) uses plain text, it creates a disconnected user experience. Bridging this gap by using the same UI library (rich) in the entry point makes the whole tool feel more cohesive and professional.
**Action:** Always check if core modules use specific CLI formatting libraries and ensure the entry points follow the same pattern for a consistent "first impression".
