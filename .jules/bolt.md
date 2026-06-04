## 2025-05-22 - [Optimizing Template Engine with Single-Pass Regex]
**Learning:** Using multiple `str.replace()` calls in a loop for template variable injection is inefficient because strings are immutable in Python, leading to O(N*V) complexity (N=length, V=variables) and many temporary objects. A single-pass `re.sub()` with a callback reduces this to O(N) and minimizes object creation.
**Action:** Always prefer `re.sub()` with a callback for template engines or multi-variable string replacements.

## 2025-05-22 - [Redundant Disk I/O in Prompt Loading]
**Learning:** Loading the same prompt files (like `00_prompt_maestro.md`) from disk for every GEM execution in a pipeline introduces unnecessary I/O latency, especially when scaling to many candidates.
**Action:** Use `@functools.lru_cache` for file-loading functions that access static assets like prompts or schemas.
