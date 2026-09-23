## 2025-05-18 - Isolated Try-Except Blocks in Pydantic Field Validators
**Vulnerability:** In input validation functions (e.g. `webhook_url` SSRF checks), placing custom `raise ValueError(...)` statements inside a broad `try ... except ValueError` block intended for `ipaddress.ip_address(hostname)` parsing causes validation exceptions to be caught and swallowed silently.
**Learning:** Broad exception handling in validator routines leads to silent security bypasses.
**Prevention:** Isolate parsing operations in minimal `try ... except` blocks and perform validation assertions in an `else` branch or after setting a parsed variable (`if ip is not None:`).
