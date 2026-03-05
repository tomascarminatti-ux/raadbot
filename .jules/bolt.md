# Bolt's Performance Journal

## 2025-05-14 - Parallel Candidate Processing
**Learning:** Sequential processing of candidates in the orchestrator is a significant bottleneck. Moving to parallel execution with asyncio.gather while ensuring the LLM client is non-blocking can drastically reduce total pipeline latency.
**Action:** Implement async support in GeminiClient and use asyncio.gather in GEM6Orchestrator.
