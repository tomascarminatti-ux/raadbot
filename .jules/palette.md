## 2025-05-15 - [Copy to Clipboard and ARIA labels]

**Learning:** [The "Copy to Clipboard" interaction in this dashboard required managing both text and icon changes to give clear feedback. Using ARIA labels for icon-only buttons like the GEM nav buttons is crucial for screen readers, but labels on non-interactive containers like footers should be avoided to reduce noise.]

**Action:** [Always add visual feedback and ARIA labels to new interactive elements. Avoid putting aria-labels on divs without roles.]
