## 2025-05-15 - Optimization of Prompt Template Building

**Learning:** Repeated disk I/O in hot paths (like `load_prompt` and `load_maestro` in every `build_prompt` call) is a major bottleneck even for small files. Additionally, multiple `.replace()` calls on large strings create unnecessary temporary string objects. A single-pass regex substitution with a callback is significantly more efficient for multi-variable template injection.

**Action:** Always use `lru_cache` for static file loading in core pipeline paths. Prefer `re.sub()` with a callback function for bulk template variable injection to achieve O(n) complexity relative to the prompt length and variable count.
