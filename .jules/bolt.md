## 2025-05-15 - Redundant State Persistence in Pipeline
**Learning:** In asynchronous pipelines with state checkpointing, sequential state updates (like usage tracking followed by result saving) often trigger multiple redundant disk writes if each sub-operation handles its own persistence. In this case, `_track_usage` was calling `_save_state` just before `_save_output` called it again.
**Action:** Consolidate state persistence at the end of the highest-level state update method (`_save_output`) to reduce I/O overhead and lock contention during parallel execution.
