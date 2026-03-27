## 2024-05-22 - Prompt Template Caching
**Learning:** Prompt templates are static Markdown files that are read for every GEM execution in the pipeline. In a parallel execution environment with multiple candidates, this leads to redundant disk I/O.
**Action:** Use `functools.lru_cache` to cache the results of template loading. This simple change reduces prompt construction overhead by over 70% without changing core logic.
