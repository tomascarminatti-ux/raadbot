## 2024-05-22 - Optimized Prompt Building

**Learning:** Replacing multiple `str.replace` calls with a single-pass `re.sub` is significantly faster for templates with many variables. However, order matters: `{{PROMPT_MAESTRO}}` must be replaced first to allow variables within it to be caught by the subsequent regex pass. Additionally, pre-serializing dictionary variables to JSON strings before the replacement loop prevents redundant computations if a variable is used multiple times.

**Action:** Use `lru_cache` for static file loading and `re.sub` with a callback for multi-variable replacement, ensuring hierarchical placeholders are handled in the correct sequence.
