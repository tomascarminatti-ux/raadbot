## 2025-05-15 - Memoization for Contract Validation
**Learning:** The orchestrator loop frequently calls `validate_contract`, which previously performed disk I/O and JSON parsing on every step. This introduced significant latency (multi-millisecond) in the reasoning loop. Implementing a simple module-level cache reduced validation time by ~25x-30x.
**Action:** Always check for repeated file reads in high-frequency loops or recursive orchestrator patterns and implement memoization for static assets like schemas or templates.
