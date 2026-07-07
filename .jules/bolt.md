## 2025-07-24 - Optimizing Prompt Construction with Hybrid Injection
**Learning:** While a single-pass `re.sub` is measurably faster than multiple `.replace()` calls ($O(N)$ vs $O(M*N)$), it prevents recursive placeholder substitution. If a base template (like a Maestro prompt) is injected and itself contains placeholders, a single-pass regex won't resolve them.
**Action:** Use a hybrid approach: perform a prioritized `.replace()` for base templates that might contain placeholders, then use a single-pass `re.sub` with a pre-compiled regex and a replacer function for all other variables. This maintains high performance while preserving template flexibility.

## 2025-07-24 - Module-level caching vs Instance method caching
**Learning:** Applying `@lru_cache` to instance methods stores a reference to `self` in the cache key. This can lead to memory leaks (as instances are never garbage collected if they remain in the cache) and inconsistent cache behavior across different instances of the same class.
**Action:** Move caching logic to module-level helper functions or use `@staticmethod` for I/O operations like schema loading, then call those helpers from within the class methods.
