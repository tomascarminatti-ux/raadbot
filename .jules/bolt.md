# Bolt's Performance Journal ⚡

Critical learnings only.

## 2025-05-14 - Optimized Prompt Construction and Schema Loading
**Learning:** iterative `str.replace` and redundant disk I/O in hot paths (like prompt building and class instantiation) significantly slow down execution. Using `lru_cache` for templates and schema loading, plus a single-pass regex for variable injection, provides ~6-7x speedup in those specific components.
**Action:** Always cache static or semi-static resources (templates, schemas) and use regex for bulk string replacements.
