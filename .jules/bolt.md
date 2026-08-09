# Bolt's Journal - Critical Learnings Only

## 2025-02-18 - [Contract Validation Caching]
**Learning:** File system metadata queries like `os.path.getmtime` are extremely lightweight (using stat system calls), whereas repeatedly opening files on disk and parsing JSON strings causes high disk I/O overhead. Implementing a dual-parameter LRU cache that keys on the file path and modification timestamp achieves a massive performance speedup while maintaining 100% cache consistency against dynamic file edits.
**Action:** Always prefer cache keys that include `mtime` to avoid stale reads from file-based caching layers.
