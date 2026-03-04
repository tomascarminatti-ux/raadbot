# Bolt's Performance Journal

## 2025-01-24 - Redundant Disk I/O in Prompt and Schema Loading
**Learning:** The application repeatedly reads prompt markdown files and JSON contract schemas from disk during pipeline execution. This introduces unnecessary latency and disk I/O pressure, especially during industrial-scale talent scraping.
**Action:** Implement `functools.lru_cache` on `load_prompt` in `agent/prompt_builder.py` and a new `_load_schema` helper in `utils/gem_core.py`. Ensure cache invalidation (`cache_clear()`) is implemented in API endpoints that modify these files (e.g., `/api/v1/gems/refine`). Redundant caching layers (e.g., caching a wrapper that calls an already-cached function) should be avoided to simplify invalidation logic.
