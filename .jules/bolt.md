## 2026-03-30 - Pre-compiling Regex Patterns in Hot Code Paths
**Learning:** In LLM output parsing (`_parse_response`) and prompt template compilation (`build_prompt`), using `re.search` or `re.findall` with regex strings causes repeated compilation overhead. Pre-compiling regexes as module-level constants (`JSON_BLOCK_RE`, `VAR_RE`) eliminates this overhead completely.
**Action:** Always pre-compile regular expressions used in hot loops or frequently executed function calls across module boundaries.
