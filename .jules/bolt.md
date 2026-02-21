## 2026-02-21 - [Parallelization with Rich]
**Learning:** `rich.console.status` (and other live displays) are not thread-safe and only one can be active at once. Attempting to run multiple candidates in parallel where each uses `console.status` leads to `Only one live display may be active at once` errors.
**Action:** Avoid simple multi-threading for CLI tools using Rich live components. For parallelization, either disable live output or use a different reporting mechanism.

## 2026-02-21 - [Micro-optimizations impact]
**Learning:** Pre-compiling JSON validators and caching static file reads (prompts) provide small but safe performance gains without architectural risks.
**Action:** Always pre-compile regexes and validators that are used in loops or repeated calls.
