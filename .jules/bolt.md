## 2025-07-14 - Optimized Prompt Building and Pipeline Initialization
**Learning:** Found that repeated disk I/O for static assets (JSON schemas, Markdown templates) and multiple string replacements in large templates were adding measurable overhead.
**Action:** Use `functools.lru_cache` for static file loading and `re.sub` with a callback for single-pass variable injection in templates.
