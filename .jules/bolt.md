## 2026-04-26 - Optimized Prompt Construction
**Learning:** Disk I/O for reading static prompt templates and repetitive regex compilation were causing measurable overhead in the prompt building process.
**Action:** Implement `lru_cache` for template loading and pre-compile regex patterns at the module level. Ensure cache invalidation is handled if templates are updated dynamically.
