## 2026-02-20 - [HIGH] Path Traversal in API Pipeline Request
**Vulnerability:** Path traversal in `search_id`, `candidate_id`, and `local_dir` fields of the `PipelineRequest` model in `api.py`.
**Learning:** Input fields used to construct file system paths were not validated, allowing attackers to potentially read or write files outside the intended `runs/` directory by using `..` sequences or absolute paths.
**Prevention:** Always validate user-supplied IDs and directory paths using strict regex (for IDs) and traversal checks (for paths). Using Pydantic's `field_validator` provides a clean way to enforce these rules at the schema level.
