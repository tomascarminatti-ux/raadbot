## 2025-05-24 - Single-pass Regex Template Engine
**Learning:** Replacing iterative `str.replace` with a single-pass `re.sub` using a callback is significantly faster (3x-10x) for template engines with many variables.
**Action:** Use `re.sub` with a lookup dictionary or callback for all future template-style string injection logic.

## 2025-05-24 - Prompt Caching Benefits
**Learning:** Caching `load_prompt` calls with `lru_cache` avoids redundant disk I/O, which is a major bottleneck in high-throughput LLM pipelines.
**Action:** Always cache static file reads that are used as templates in agentic workflows.
