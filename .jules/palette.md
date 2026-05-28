# Palette's UX Journal

This journal documents critical UX and accessibility learnings.

## 2025-05-24 - Initial Journal Creation
**Learning:** Initialized the journal to track micro-UX improvements and accessibility wins.
**Action:** Use this journal to document significant UX insights throughout the project.

## 2025-05-24 - Log File Pollution
**Learning:** Local log files like `server.log` can accidentally be included in commits if not careful, polluting the PR with environment-specific noise.
**Action:** Always check `git status` before committing and ensure runtime logs are ignored or reverted.
