## 2025-05-14 - Path Traversal in Identifier-based Paths
**Vulnerability:** Path traversal via `search_id`, `gem_id`, and `local_dir` inputs. Attackers could create directories outside the `runs/` folder or potentially read/write files outside the `prompts/` directory.
**Learning:** Using `os.path.join` with unsanitized user input is insufficient to prevent path traversal in Python; if a component of the path is an absolute path or contains '..' segments, it can lead to access outside the intended base directory.
**Prevention:** Apply strict regex validation (`^[a-zA-Z0-9_-]+$`) to all identifier-based inputs used in file paths. For directory inputs, explicitly reject `..` segments and leading slashes.
