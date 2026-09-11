## 2026-03-29 - [mtime-based LRU Caching for Prompt Templates]
**Learning:** Keying `functools.lru_cache` on `(filepath, mtime)` eliminates repetitive disk file I/O operations when loading prompt templates across repeated LLM runs, while automatically invalidating the cache as soon as prompt files are updated on disk.
**Action:** Use `(filepath, mtime)` tuples for caching disk asset loaders across LLM prompt builder functions.
