# Bolt's Performance Journal

## 2025-05-15 - Prompt Building Optimization
**Learning:** String concatenation and repeated `str.replace` in a loop create $O(N \times M)$ complexity and multiple intermediate string copies. `re.sub` with a callback function allows for a single-pass replacement ($O(N)$), which is significantly more efficient for template injection. Additionally, `lru_cache` is essential to avoid redundant Disk I/O for static or slow-changing assets like prompt templates.
**Action:** Use `re.sub` with a dictionary-lookup callback for bulk template variable replacement and apply `lru_cache` to file loading functions in the agent's core path.
