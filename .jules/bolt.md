## 2025-05-15 - Prompt Template Caching
**Learning:** In high-throughput multi-agent systems, redundant disk I/O for static prompt templates is a silent performance killer. Caching templates with `lru_cache` significantly reduces latency during batch processing.
**Action:** Always implement caching for static assets like prompt templates and ensure cache invalidation is handled when those assets are updated via API.
