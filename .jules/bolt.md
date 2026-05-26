# Bolt Performance Journal ⚡

## 2024-05-24 - Efficient Template Rendering with Caching and Regex
**Learning:** In LLM-driven pipelines, prompt construction can become a micro-bottleneck if it involves frequent file I/O and multiple string replacements per request. Using `functools.lru_cache` for static template loading and a single-pass `re.sub` for variable injection significantly reduces CPU and I/O overhead.
**Action:** Always prefer single-pass regex substitution over multiple `.replace()` calls for template engines. Implement caching for static assets like prompt markdown files.
