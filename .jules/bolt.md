## 2025-05-22 - Initial Journal Entry
**Learning:** Initializing Bolt's performance journal for Raadbot.
**Action:** Focus on identifying measurable bottlenecks in the current architecture.

## 2025-05-22 - Single-pass Regex Replacement & Caching
**Learning:** Iterative string replacement with `str.replace` in a loop is (N \cdot M)$. Using `re.sub` with a callback function reduces it to (M)$ and prevents double-expansion bugs. Combining this with `lru_cache` for disk I/O provides a massive speedup for prompt construction.
**Action:** Always prefer single-pass replacement for template engines and cache static file reads.
