# Bolt's Performance Journal ⚡

## 2025-05-14 - Optimized Prompt Construction
**Learning:** Prompt construction was a significant overhead due to redundant disk I/O (reading the same template files multiple times per agent invocation) and sequential string replacements. Caching templates with `lru_cache` and using a single-pass `re.sub` for variable injection provides a measurable ~5x speedup in prompt preparation.
**Action:** Always use the cached `load_prompt` and favor single-pass regex replacement for multi-variable template injection.

## 2025-05-14 - Benchmarking Safety
**Learning:** Running benchmark scripts that overwrite files in `prompts/` can accidentally destroy the core logic of the application (System Prompts).
**Action:** When benchmarking, use temporary directories or mock file systems to avoid overwriting real production templates. Always verify and restore critical prompt files if they were touched during testing.
