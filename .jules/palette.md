## 2025-05-14 - Visual Feedback for Clipboard Actions
**Learning:** Providing immediate visual feedback for asynchronous background operations (e.g., changing 'Copy' to '¡Copiado!' on a clipboard button) significantly reduces user uncertainty and enhances the perceived responsiveness of the interface.
**Action:** Always implement a success state (icon/text change) for utility buttons like 'Copy' or 'Save'.

## 2025-05-14 - Semantic Input Association
**Learning:** When visual labels are omitted or stylized as headers in a dashboard, explicit association via `aria-labelledby` is critical for maintaining semantic clarity for screen reader users.
**Action:** Use `aria-labelledby` to associate inputs with their section headers when standard `<label>` elements are not used for layout reasons.
