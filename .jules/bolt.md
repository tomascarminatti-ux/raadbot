# ⚡ Bolt's Performance Journal

## 2025-05-15 - Optimizing Prompt Construction
**Learning:** Multiple string scans and copies with `str.replace()` in a loop create a (N \cdot M)$ bottleneck for prompt building. Moving to a single-pass regex substitution with `re.sub()` and pre-serializing variables to JSON reduces latency by ~4x.
**Action:** Use single-pass regex patterns for template substitution instead of multiple replace calls.

## 2025-05-15 - Prompt Template I/O
**Learning:** Reading static prompt templates from disk for every GEM execution is redundant. Using `functools.lru_cache` for template loading significantly reduces I/O overhead.
**Action:** Cache static configuration and template files that don't change during process execution.
