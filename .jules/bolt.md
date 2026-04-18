## 2024-05-18 - [Pipeline State Write Bottleneck]
**Learning:** Redundant disk writes in `agent/pipeline.py` were caused by `_track_usage` calling `_save_state` every time, even when called from `_save_output` which also calls `_save_state`. This significantly slows down parallel execution of candidates as they fight for the disk lock.
**Action:** Remove intermediate `_save_state` calls when the state update is part of a larger atomic operation that already persists state.

## 2024-05-18 - [Prompt Building Overhead]
**Learning:** Using multiple `str.replace` calls in a loop for prompt variable injection is inefficient for large templates with many variables. A single-pass `re.sub` with a mapping function is much faster.
**Action:** Use regex-based single-pass replacement for template engines.
