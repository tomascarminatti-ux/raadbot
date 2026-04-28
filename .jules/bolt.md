## 2025-05-15 - Prompt Construction and Disk I/O Optimization

**Learning:** Prompt templates were being read from disk on every GEM execution. By implementing `functools.lru_cache` and pre-compiling the variable substitution regex, construction latency was reduced by ~80% (from ~0.17ms to ~0.03ms). Additionally, the pipeline was performing two disk writes per GEM stage (one for usage tracking and one for state updates); consolidating these into a single atomic transaction inside the `asyncio.Lock` block reduced I/O overhead and improved atomicity.

**Action:** Always check for redundant disk I/O in frequently called "save" or "load" functions. Use `lru_cache` for static assets like templates.
