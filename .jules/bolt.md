## 2025-05-14 - Prompt Builder Optimization Regression
**Learning:** Moving to a single-pass `re.sub` for variable substitution in templates with nested includes (like `{{PROMPT_MAESTRO}}`) causes a regression if the included template also contains variables. The included content is injected *after* the scanner has already passed its position, so its own variables remain unreplaced.
**Action:** Always perform template inclusion (like maestro prompts) as a separate first pass before applying the final variable substitution pass to ensure the entire combined content is processed.

## 2025-05-14 - Disk I/O Bottleneck in Utility Modules
**Learning:** Core utility functions like `load_prompt` that are called multiple times per request can become a bottleneck due to redundant disk I/O. Even small files benefit from caching if accessed frequently in a high-concurrency or high-iteration environment.
**Action:** Use `functools.lru_cache` on functions that read static configuration or template files from disk.
