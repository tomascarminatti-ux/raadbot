## 2025-05-15 - [Optimize prompt building with caching and pre-compilation]
**Learning:** Caching disk I/O for static templates and pre-calculating common string operations (like injecting a master prompt into specific templates) significantly reduces overhead in LLM-heavy pipelines. Pre-compiling regex patterns further minimizes per-call latency.
**Action:** Always check for repeated file reads or redundant string manipulations in core utility modules. Apply `lru_cache` and pre-compile regexes for immediate performance gains in high-frequency functions.
