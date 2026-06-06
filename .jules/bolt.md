## 2025-05-15 - [Optimize Prompt Builder]
**Learning:** Disk I/O for prompt templates and (V \cdot L)$ string substitution in  were causing unnecessary latency (~0.11ms per call).
**Action:** Implement `lru_cache` for disk-bound operations and use single-pass `re.sub` with a callback for template variable injection to achieve (L)$ complexity, reducing latency to ~0.02ms.
## 2025-05-15 - [Optimize Prompt Builder]
**Learning:** Disk I/O for prompt templates and $O(V \cdot L)$ string substitution in `build_prompt` were causing unnecessary latency (~0.11ms per call).
**Action:** Implement `lru_cache` for disk-bound operations and use single-pass `re.sub` with a callback for template variable injection to achieve $O(L)$ complexity, reducing latency to ~0.02ms.
