## 2025-05-18 - LRU Caching for Prompt Loading
**Learning:** `load_prompt` and `load_maestro` in `agent/prompt_builder.py` are called repeatedly during pipeline operations, reading prompt markdown files from disk every time. Decorating a helper function with `@functools.lru_cache(maxsize=32)` and supplying `os.path.getmtime(filepath)` eliminates redundant disk reads while guaranteeing automatic cache invalidation when prompt files are modified.
**Action:** Use `mtime`-keyed `@functools.lru_cache` for disk-based template or file loaders across Python modules.
