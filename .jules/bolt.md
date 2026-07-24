# Bolt Optimization Journal

## 2025-02-15 - File Invalidation with LRU Cache
**Learning:** Decorating file-modification-time (mtime) lookup helpers with `lru_cache` cache-locks file change checking, completely bypassing disk update detection.
**Action:** Keep the mtime lookup function side-effect free and uncached, using it solely to provide the dynamic key parameter to the cached resource loading helper.

## 2025-02-15 - Prefix Conflict in Single-Pass Regex Replace
**Learning:** During single-pass string template replacement, key collision or prefix matching conflicts can occur if a shorter variable is a prefix of a longer variable.
**Action:** Sort pattern keys by length descending (`sorted(keys, key=len, reverse=True)`) before compiling the joint regex replacement pattern.
