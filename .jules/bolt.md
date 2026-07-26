# Bolt's Journal - Critical Learnings

## 2025-02-15 - Mtime Caching & Single-Pass Regex
**Learning:** When implementing file-modification-time (mtime) based cache invalidation using `@functools.lru_cache`, avoid decorating the function that retrieves `mtime` directly (e.g., `os.path.getmtime`), as this will cache the `mtime` value itself and miss any disk modifications. Additionally, when using `re.sub` for single-pass replacement of multiple template variables, sort the keys by length descending to prevent prefix matching conflicts, and construct the pattern using regular raw strings rather than f-strings to avoid complex brace escaping syntax errors.
**Action:** Implement `_load_prompt_cached` and `_load_contract` as pure cached helpers accepting path and `mtime` arguments, retrieving `os.path.getmtime` outside the cache decorator, and build raw regex strings like `r"\{\{\s*" + re.escape(k) + r"\s*\}\}"` instead of `rf"..."` to be 100% robust.
