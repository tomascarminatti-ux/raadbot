## 2025-05-14 - [XSS and Localization Consistency]
**Learning:** Dynamic UI rendering using `innerHTML` to set attributes like `aria-label` can introduce XSS vulnerabilities. Additionally, inconsistent localization (mixing English and Spanish) creates a disjointed experience for screen reader users.
**Action:** Always use safe DOM APIs (`createElement`, `textContent`) for dynamic content and ensure all UI strings follow the user's primary language preference (Spanish in this repo).
