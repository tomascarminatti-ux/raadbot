# Bolt's Performance Journal

## 2026-03-01 - JSON Schema Pre-compilation and Prompt Caching
**Learning:** In highly repetitive workflows, such as sequential pipelines analyzing multiple candidates, reconstructing the validator class and parsing the JSON schema on every single run of `jsonschema.validate` adds significant runtime overhead (~2.62 ms per call). Pre-compiling the validator class using `jsonschema.validators.validator_for` on class initialization reduces the validation overhead to ~0.18 ms (a ~14x speedup). Additionally, file I/O operations for reading prompt templates from disk on every invocation of `build_prompt` can be completely eliminated using `functools.lru_cache`, resulting in a ~200x speedup for prompt loading.
**Action:** Always pre-compile JSON schema validators when validating multiple instances of the same schema, and cache static configuration/prompt files that do not change during runtime using `functools.lru_cache`.
