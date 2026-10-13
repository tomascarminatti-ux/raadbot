# Bolt's Journal - Critical Performance Learnings

## 2026-03-30 - Prompt Template LRU Caching and Regex Pre-compilation
**Learning:** Frequent file I/O operations when loading system prompt templates in `load_prompt()` cause noticeable delay during pipeline construction. Decorating an internal file loading helper with `@functools.lru_cache(maxsize=32)` keyed on file path and modification timestamp (`mtime`) eliminates disk I/O while automatically invalidating cache upon template file updates. Pre-compiling `VAR_RE = re.compile(r"\{\{(\w+)\}\}")` further avoids repeated regex compilation overhead.
**Action:** Use `@functools.lru_cache` on file helper methods with `os.path.getmtime` for file-backed templates/schemas, and pre-compile regular expressions at module scope.
