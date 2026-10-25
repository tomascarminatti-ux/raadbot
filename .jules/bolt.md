## 2025-05-18 - Prompt Template Loading LRU Caching
**Learning:** Prompt templates are rendered frequently during GEM orchestration loops. Caching file reads with `@functools.lru_cache` keyed on `(filepath, mtime)` using `os.path.getmtime(filepath)` eliminates repeated disk reads while ensuring prompt modifications (e.g. from `/api/v1/gems/refine`) automatically invalidate the cache without stale state.
**Action:** Apply `mtime`-keyed LRU caching for static or editable file assets across agent modules.
