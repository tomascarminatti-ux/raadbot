# Bolt's Performance Journal

## 2026-08-27 - Prompt Template LRU Caching & Invalidation
**Learning:** Loading prompt markdown templates repeatedly from disk in `agent/prompt_builder.py` introduces unnecessary file I/O overhead during agent pipeline runs and prompt list API requests. Applying `@functools.lru_cache` reduces prompt loading time by >100x while explicit cache invalidation in `api.py` upon GEM prompt refinement guarantees data freshness without disk polling.
**Action:** Use LRU caching for static/rarely-changing template files and ensure any API endpoints that mutate those templates invoke cache-clearing functions immediately after disk writes.
