## 2025-05-15 - [Prompt Builder Optimization]
**Learning:** Disk I/O for static templates and iterative `.replace()` calls for variable injection created a measurable bottleneck (0.12ms per call). Single-pass regex substitution (`re.sub` with a callback) is significantly more efficient ($O(N)$ vs $O(N \times M)$) and prevents accidental double-replacement.
**Action:** Use `lru_cache` for template loading and `re.sub` for batch variable replacement in text processing pipelines. Ensure nested placeholders (like `PROMPT_MAESTRO`) are resolved before the main substitution pass.
