## 2025-05-15 - [Nested Template Resolution in re.sub]
**Learning:** Replacing iterative `.replace()` calls with a single-pass `re.sub` for template resolution provides significant speedups but breaks nested variable expansion if not handled carefully. Placeholders like `{{PROMPT_MAESTRO}}` that inject other placeholders must be expanded before the final regex pass.
**Action:** Always check for hierarchical or nested template structures before moving to a single-pass replacement strategy. Expand parent templates first or use a recursive replacement function if necessary.
