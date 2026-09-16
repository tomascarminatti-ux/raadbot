## 2026-03-30 - Path Traversal Prevention in API Request Schemas
**Vulnerability:** Unsanitized user inputs in request fields (`search_id`, `candidate_id`, `gem_id`, `local_dir`) could be passed to file system operations like `os.path.join`, enabling directory traversal.
**Learning:** In Pydantic models, `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` should be preferred over `re.match` with `$` because `$` allows trailing newline characters (`\n`). Additionally, `local_dir` paths should normalize backslashes and disallow relative directory traversal components (`..`) or absolute path prefixes.
**Prevention:** Apply strict Pydantic `@field_validator` checks on all request fields that influence filesystem paths before reaching endpoint handlers.
