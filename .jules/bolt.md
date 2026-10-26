# Bolt's Performance Journal

## 2026-03-31 - Prompt Template Loading LRU Caching
**Learning:** System prompt files in `prompts/*.md` were previously read synchronously from disk on every `build_prompt` call during multi-step orchestration workflows (e.g. GEM6). Decorating helper `_load_prompt_cached` with `@functools.lru_cache(maxsize=32)` keyed by file path and `mtime` eliminates disk I/O while automatically invalidating when files change on disk (such as via AI prompt refinement endpoints).
**Action:** Use `mtime`-aware `@functools.lru_cache` when caching local file resources that might occasionally be updated at runtime.

## 2026-03-31 - Restricting Pytest Discovery Paths & Submodule Cleanup
**Learning:** Configuring `testpaths = tests` in `pytest.ini` prevents pytest from discovering root-level integration test scripts like `test_gemini.py` in CI, avoiding unexpected live network connection failures. Guarding top-level script logic with `if __name__ == '__main__':` prevents unwanted side effects during import. Unreferenced git submodule index entries (such as `zeroclaw`) without `.gitmodules` mappings cause `git submodule foreach` failures during GitHub Actions post-job cleanup and should be removed with `git rm -f`.
**Action:** Always set `testpaths` in `pytest.ini`, guard script execution in root-level `.py` files, and clean up unreferenced submodule index entries.
