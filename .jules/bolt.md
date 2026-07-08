# Bolt's Journal - Critical Learnings

## 2025-05-15 - [Prompt Construction Optimization]
**Learning:** In LLM pipelines that build prompts for many candidates using static templates, file I/O and iterative string replacements become a significant bottleneck. Using `lru_cache` for template loading and a single-pass `re.sub` for variable injection can provide order-of-magnitude speedups.
**Action:** Always use caching for static templates and prefer single-pass regex substitution for multi-variable template injection.

## 2025-05-15 - [Environment Dependencies]
**Learning:** The sandbox environment might lack critical dependencies for running tests (e.g. `google-auth-oauthlib`, `pandas`).
**Action:** If tests fail with `ModuleNotFoundError`, proactively install common project dependencies.
