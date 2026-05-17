## 2025-05-24 - Initial Bolt Journal
**Learning:** This codebase uses a pipeline that processes candidates in parallel, making it sensitive to blocking I/O and redundant operations in the hot path of GEM execution.
**Action:** Prioritize optimizations that reduce disk I/O and redundant template processing in the pipeline.
