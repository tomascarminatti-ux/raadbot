## 2026-03-31 - Cache prompt file loads with mtime invalidation

**Learning:** Prompt template files in `prompts/` were read from disk on every `load_prompt` invocation, including repeated reads of `00_prompt_maestro.md` for every `build_prompt` call. Using `@functools.lru_cache(maxsize=32)` on a helper keyed by `(filepath, mtime)` provides a ~6x speedup while guaranteeing live updates if prompt files are edited on disk.
**Action:** Use `os.path.getmtime` as a cache parameter key when caching disk reads for static or infrequently modified files in Python.
