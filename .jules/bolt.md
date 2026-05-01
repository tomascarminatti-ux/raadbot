## 2026-05-01 - Single-Pass Regex Substitution for Prompts
**Learning:** Using `re.sub` with a callback for variable substitution in prompt templates is significantly more efficient than nested loops or multiple `.replace()` calls, especially as the number of variables or the template size increases. Moving `import` statements (e.g., `import json`) out of loops and to the module level avoids redundant lookup overhead in high-frequency functions.
**Action:** Always prefer `re.sub` with a dictionary-based callback for template engines. Pre-compile the regex at the module level.
