## 2025-05-24 - Contextual Feedback and Guarded States

**Learning:** Providing immediate visual feedback for asynchronous utility operations (like "Copy to Clipboard") significantly enhances perceived responsiveness. However, rapid repeated clicks during the feedback state can cause UI flickering or state race conditions.

**Action:** Implement a `dataset` guard (e.g., `btn.dataset.copying = 'true'`) to ignore redundant clicks while the feedback state is active. Additionally, hide contextual utility buttons until the content they operate on is actually available to prevent "empty" interactions.
