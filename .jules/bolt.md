## 2025-05-24 - Destructive Benchmarking
**Learning:** Benchmarking scripts that overwrite production prompt templates (e.g., `prompts/gem1.md`) with dummy data can "lobotomize" the agent if those changes are accidentally committed. This happened because the benchmark logic used `write_file` on production paths instead of temporary ones.
**Action:** When writing benchmarks, always use temporary directories or mock file I/O to ensure production assets are never modified. Always verify `git status` before requesting a review to ensure no unexpected file modifications (like prompt deletions) are included.

## 2025-05-24 - String concatenation in loops
**Learning:** The `build_prompt` function was using `str.replace` in a loop, which creates a new string object for each replacement. For large prompts with many variables, this is O(N*M).
**Action:** Use a single-pass `re.sub` with a callback for variable replacement. This is O(N) and significantly reduces memory allocations and latency (~8.6x speedup).
