## 2025-05-15 - Caching and Regex Optimization for Prompt Building
**Learning:** Significant performance gains (~24x-30x) were achieved by caching template/schema I/O and using single-pass regex for variable injection. Caching the intermediate state of pre-merged templates (Maestro + GEM) further reduces string processing overhead.
**Action:** Always prioritize caching for static I/O assets and use `re.sub` with a callback for complex multi-variable string templates instead of iterative `.replace()` calls.

## 2025-05-15 - Dangerous Verification Scripts
**Learning:** Standalone verification scripts that modify production-shared directories (like `prompts/`) can lead to catastrophic data loss if they overwrite core files (e.g., `00_prompt_maestro.md`) without proper isolation or backup.
**Action:** Use temporary directories (`tempfile`) or mock file systems for testing logic that interacts with the disk, and never use production file names in verification scripts.
