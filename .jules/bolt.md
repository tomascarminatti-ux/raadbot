## 2025-05-15 - Regex-based Single-pass Variable Substitution

**Learning:** Using `re.sub` with a callback for variable substitution in prompt templates is significantly more efficient than nested loops or multiple `.replace()` calls, especially as the number of variables or the template size increases. It also prevents accidental recursive substitution if a variable's value contains a placeholder.

**Action:** Prefer `re.sub` with a mapping function/callback for template systems instead of iterative replacements.

## 2025-05-15 - LRU Cache for Template I/O

**Learning:** Prompt templates are often read multiple times during a single pipeline execution (e.g., for every candidate). `functools.lru_cache` on the loading function effectively eliminates redundant disk I/O with minimal memory overhead.

**Action:** Cache file-based configuration or templates that are frequently accessed but rarely changed during execution.
