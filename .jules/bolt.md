## 2025-05-15 - Prompt Construction Optimization
**Learning:** Using 're.sub' with a callback for variable substitution in prompt templates is significantly more efficient than nested loops or multiple '.replace()' calls ((N)$ vs (K \cdot N)$), especially as the number of variables or the template size increases. Additionally, caching static assets like prompt templates with 'lru_cache' eliminates redundant disk I/O.
**Action:** Use single-pass regex substitution and 'lru_cache' for templating systems and frequently accessed static files.
