## 2025-05-14 - CI Collection Failure with Non-Test Scripts
**Learning:** Pytest might attempt to collect and execute scripts outside of `tests/` if they don't have proper guards. Scripts like `test_gemini.py` that perform live API calls or connection-dependent logic must be protected with `if __name__ == "__main__":` to avoid CI failures during test discovery.
**Action:** Always wrap execution logic in standalone scripts with `if __name__ == "__main__":` and ensure temporary log files are added to `.gitignore`.
