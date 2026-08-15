## 2026-03-30 - Cache JSON Contract Schemas for Fast Validation
**Learning:** In GEM orchestrations, contract schemas are stored on disk as JSON files and loaded repeatedly during step validations (`validate_contract`). Using `@functools.lru_cache(maxsize=32)` on a helper loading function avoids re-opening files and re-parsing JSON strings on every call.
**Action:** Always wrap static JSON schema loads with `lru_cache` when evaluated in hot loops or pipeline step validations.
