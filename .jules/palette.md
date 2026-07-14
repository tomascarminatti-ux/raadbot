## 2025-05-15 - Improving Code Block Accessibility and Clipboard UX

**Learning:** Adding `tabindex="0"` and `aria-label` to `<pre>` tags is essential for keyboard users to scroll through long code content. Additionally, visual feedback for clipboard actions (like changing button text/color) significantly improves user confidence, but these states must be explicitly reset when the user switches context (e.g., changing the active module) to maintain UI consistency. Testing these features in headless environments requires granting explicit `clipboard-read`/`clipboard-write` permissions to the browser context.

**Action:** Always include keyboard scroll support for overflow containers and ensure temporary UI feedback states are tied to the lifecycle of the displayed data.
