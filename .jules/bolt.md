## 2025-05-15 - Single-Pass Template Substitution
**Learning:** In LLM prompt construction, repeatedly calling `str.replace()` for each variable in a template is O(V * N) where V is the number of variables and N is the prompt length. This also results in multiple temporary string allocations.
**Action:** Use a single `re.sub()` pass with a callback function to achieve O(N) complexity and minimize string allocations. This is especially effective when combined with `lru_cache` for prompt files to eliminate disk I/O.
