## 2025-05-23 - Path Traversal in Prompt Refinement
**Vulnerability:** The `/api/v1/gems/refine` endpoint constructed file paths using raw user input (`gem_id`), allowing arbitrary file reads/writes outside the `prompts/` directory.
**Learning:** Using string interpolation for file paths without validation or whitelisting is dangerous even if a prefix is provided.
**Prevention:** Use a hardcoded whitelist for allowed file identifiers and strictly validate all identifier strings using a safe regex pattern.
