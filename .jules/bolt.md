## 2025-05-15 - [Safe Benchmarking]
**Learning:** Benchmarking scripts that modify prompt templates or data files should never use production directories (like `prompts/`). Overwriting these files can lead to critical regressions if not caught.
**Action:** Always use a temporary directory or mock the filesystem when a benchmark requires file writes. Use `git checkout` to restore any accidentally modified tracked files.

## 2025-05-15 - [Efficient Variable Substitution]
**Learning:** In Python, a loop of `str.replace()` calls for template variable substitution is O(N*M) where N is the number of variables and M is the string length. Using `re.sub()` with a callback function allows for a single-pass replacement, which is significantly faster for large templates or many variables.
**Action:** Use `re.sub(pattern, callback, text)` for efficient multi-variable template rendering.
