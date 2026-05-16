## 2024-05-23 - Accessibility and Utility Feedback Patterns

**Learning:** When visual labels are omitted in the dashboard interface, input elements should be associated with their respective headers using `aria-labelledby` to maintain semantic clarity for screen readers. Additionally, providing immediate visual feedback for asynchronous operations (like clipboard copy) significantly reduces user uncertainty. Using a `data-` attribute as a guard prevents visual flickering and state race conditions during rapid user interaction.

**Action:** Always link inputs to headers with `aria-labelledby` if no `<label>` is present. Implement feedback states (e.g., 'Copiado!') with a state guard for all utility buttons.
