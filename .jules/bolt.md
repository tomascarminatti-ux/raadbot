## 2025-05-15 - [Efficient Prompt Variable Injection]
**Learning:** Using multiple `.replace()` calls in a loop for variable injection is $O(N \cdot M)$. A single-pass `re.sub` with a callback is significantly faster and more scalable as the number of variables or prompt size grows.
**Action:** Always prefer `re.sub` for bulk variable replacement in templates.

## 2025-05-15 - [Redundant Disk Writes in Async Pipelines]
**Learning:** In async pipelines with state persistence, calling `_save_state()` in low-level utility methods (like `_track_usage`) that are always wrapped by higher-level methods that ALSO call `_save_state()` leads to $2x$ disk I/O overhead.
**Action:** Audit call stacks for state-saving methods to ensure one high-level call persists all accumulated changes.
