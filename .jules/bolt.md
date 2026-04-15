## 2025-04-15 - [Template Processing Bottleneck]
**Learning:** The previous implementation of `build_prompt` used a loop with multiple `str.replace` calls and repeated disk reads for the maestro prompt, leading to O(V * N) complexity where V is the number of variables.
**Action:** Use `functools.lru_cache` for static assets like prompt templates and `re.sub` with a replacer function for single-pass variable injection to achieve O(N) complexity.
