## 2025-05-24 - Single-pass Optimization vs. Template Inheritance
**Learning:** When optimizing template engines from O(N*M) loop-based replacements to an O(M) single-pass regex replacement, nested templates (like a base prompt containing placeholders) will break if not handled carefully. Single-pass `re.sub` does not recursively scan newly injected content.
**Action:** Always identify "meta" or "base" templates that contribute new placeholders and expand them *before* the final single-pass variable replacement.
