## 2024-05-05 - Prompt Construction Optimization
**Learning:** In a multi-agent orchestrator, repeated disk I/O and multiple string scan passes for variable replacement in prompt templates becomes a measurable bottleneck (~0.16ms per call).
**Action:** Implement `lru_cache` for template loading and single-pass `re.sub` for variable injection. Performance improved ~12x (~0.013ms per call).
