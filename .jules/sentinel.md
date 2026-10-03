## 2025-05-18 - [Pydantic Input Validation for Directory Traversal & SSRF Prevention]
**Vulnerability:** Unsanitized user inputs in API models allowed arbitrary file system path traversal (`search_id`, `candidate_id`, `local_dir`, `gem_id`) and SSRF vectors via `webhook_url`.
**Learning:** FastAPI endpoints that pass string inputs directly to file system utilities (`os.path.join`, `open()`) or HTTP clients (`httpx.post`) can lead to arbitrary file disclosure and SSRF if input fields are not validated at model initialization.
**Prevention:** Always enforce strict alphanumeric regex (`re.fullmatch(r"^[a-zA-Z0-9_-]+$")`) on string identifiers and validate IP/host destinations against loopback and private IP blocks using `ipaddress` and `urllib.parse` in Pydantic field validators.
