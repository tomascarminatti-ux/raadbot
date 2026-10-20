## 2025-02-18 - Isolated Exception Handling in Pydantic Field Validators
**Vulnerability:** Broad exception handling in custom Pydantic validators can accidentally swallow `ValueError` exceptions raised for invalid inputs or security violations.
**Learning:** Catching broad `except ValueError` when utilizing helper functions like `ipaddress.ip_address` or parsing logic can intercept custom `raise ValueError` assertions, causing validation to pass silently or fail unexpectedly.
**Prevention:** Always isolate try/except blocks tightly around third-party or library helper functions when validating fields in Pydantic models.

## 2025-02-18 - Full Match Regex Validation for Identifiers
**Vulnerability:** Using `re.match` with `$` in regex validation allows trailing newline characters (`\n`) at the end of input strings, potentially leading to path manipulation or header/log injection.
**Learning:** `$` matches before a newline at the end of the string in Python `re`.
**Prevention:** Use `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` for strict identifier validation.
