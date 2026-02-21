## 2025-02-21 - [Prompt Loading Redundancy]
**Learning:** The agentic pipeline architecture repeatedly loads the same static prompt templates (especially the large `00_prompt_maestro.md`) for every GEM step of every candidate. This creates significant redundant disk I/O that scales linearly with the number of candidates.
**Action:** Use `@functools.lru_cache` for template loading functions and move imports outside of hot loops in `prompt_builder.py`.

## 2025-02-21 - [JSON Schema Validation Overhead]
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly is ~60x slower than using a pre-compiled `Draft7Validator` instance, as it re-parses the schema on every call.
**Action:** In long-running processes (like the FastAPI server), instantiate the validator once and reuse it for all candidate validations.
