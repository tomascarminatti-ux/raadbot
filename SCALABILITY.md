# Future Scalability & Cost Control Strategy

## 📈 Scalability Roadmap
1. **Phase 1: Local Industrial (Current)**
   - SQLite, Docker Compose, Single Host.
2. **Phase 2: Distributed Production**
   - **DB**: Migrate to PostgreSQL (change connection string in `infra/db/api.py`).
   - **Agents**: Deploy each agent as a separate service in Kubernetes/ECS.
   - **Queueing**: Use RabbitMQ or Redis between agents to handle high concurrency.
3. **Phase 3: Data Warehouse**
   - Stream `discovery_logs` and `entity_state` to BigQuery/Snowflake for long-term audit.

## 💸 Cost Control Tactics
1. **Aggressive Scoring (GEM2)**:
   - Run a cheap, fast model for initial scoring.
   - Only use high-IQ models (GEM3/4) for items that pass the score cutoff (e.g., > 0.4).
2. **Caching**:
   - Implement `entity_id` hashing to skip processing if context hasn't changed.
3. **Token Limits**:
   - `GEM6` strictly rejects results exceeding predefined token usage.
4. **Batch Processing**:
   - Periodically run `sheets_dump.py` instead of per-transaction to save API quota.
