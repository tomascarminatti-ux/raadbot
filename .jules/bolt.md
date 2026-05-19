# BOLT JOURNAL - CRITICAL LEARNINGS ONLY

## 2025-05-22 - Prompt Builder Optimization Baseline
**Learning:** The `build_prompt` function in `agent/prompt_builder.py` is a frequent operation that performs repeated disk I/O and iterative string replacements. Baseline measurement shows ~0.1281ms per call.
**Action:** Implement `lru_cache` for template loading and switch to single-pass regex substitution to minimize overhead.
