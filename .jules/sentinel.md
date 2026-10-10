## 2025-05-20 - Broad Exception Handling in Pydantic Field Validators Swallowing Custom Validation Errors
**Vulnerability:** Input validation for SSRF in `webhook_url` failed to reject loopback/private IP addresses because a broad `except ValueError` wrapped both `ipaddress.ip_address(hostname)` and the custom `raise ValueError(...)`.
**Learning:** Placing custom `raise ValueError(...)` statements inside a `try:` block with an `except ValueError` catch causes Python to catch its own validation error and execute `pass`, silently failing the security check.
**Prevention:** Narrowly isolate function calls that can throw exceptions (such as `ipaddress.ip_address`) inside `try:` blocks, and place custom `raise ValueError(...)` error assertions outside the `try:` block.
