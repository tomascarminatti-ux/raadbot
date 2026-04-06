## 2025-05-22 - [Optimizing JSON Validation and Prompt Construction]
**Learning:** `jsonschema.validate` is expensive as it compiles the schema on every call (~2.6ms). Pre-compiling the validator and caching it reduces this to ~0.2ms. Similarly, `str.replace` in a loop for prompt construction creates multiple large string copies; a single-pass `re.sub` with a callback is significantly more efficient (~82% improvement).
**Action:** Always pre-compile validators for repeated data validation and use single-pass regex substitution for template-like string building.

## 2025-05-22 - [Testing Anti-pattern: Overwriting Production Configs]
**Learning:** Modifying production files (like `prompts/`) during unit test `setUp` can lead to critical regressions if those changes are accidentally committed.
**Action:** Use `unittest.mock.patch` or temporary directories for file-based tests to ensure production assets remain untouched.
