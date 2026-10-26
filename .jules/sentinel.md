## 2025-05-18 - Swallowed Exception in Pydantic Field Validator
**Vulnerability:** Broad `try...except ValueError` blocks in Pydantic `@field_validator` functions when parsing IP addresses.
**Learning:** Wrapping both `ipaddress.ip_address(host)` parsing and the custom `raise ValueError(...)` assertion inside the same `try...except ValueError:` block causes the validator's own `ValueError` to be caught and swallowed, silently allowing invalid/restricted inputs (such as SSRF payloads) to pass validation.
**Prevention:** Narrowly isolate the helper call (e.g. `ipaddress.ip_address`) inside the `try...except ValueError` block to set a variable or flag, and perform the `raise ValueError(...)` validation check outside the exception handler block.
