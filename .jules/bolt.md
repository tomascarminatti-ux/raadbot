## 2025-05-22 - Optimized Prompt Builder Latency

**Learning:** The original `build_prompt` implementation used a loop of `str.replace()` calls for variable substitution, resulting in $O(N \times M)$ complexity where $N$ is the number of variables and $M$ is the prompt length. Additionally, it performed redundant disk I/O by loading the prompt and maestro templates from the filesystem on every call.

**Action:** Implemented `@lru_cache` for template loading to eliminate redundant I/O and refactored variable substitution to use a single-pass `re.sub()` with a callback function, reducing complexity to $O(M)$. This resulted in a ~9.5x latency reduction (from ~0.198ms to ~0.021ms per call).
