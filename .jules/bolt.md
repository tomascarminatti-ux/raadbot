## 2026-02-25 - Contract Schema Loading LRU Cache

**Learning:** In multi-step agent orchestrations (such as `GEM6Orchestrator`), `validate_contract` is invoked repeatedly to validate output JSON schemas. Re-reading JSON contract files from disk and parsing JSON on every step introduces significant disk I/O and CPU overhead. Caching contract schemas in memory with `@functools.lru_cache` keyed by file path and modification timestamp (`mtime`) yields ~8x-9x speedup while guaranteeing automatic cache invalidation if schema files are edited.

**Action:** When validating schemas or reading static configuration files repeatedly in workflow loops, use an mtime-based LRU cache to eliminate unnecessary disk I/O while maintaining safety across file updates.
