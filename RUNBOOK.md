# GEM v3.0 Operational Runbook

## 🚀 Startup Procedure
1. **Initialize Environment**:
   ```bash
   cp .env.example .env
   # Ensure config/service_account.json is present for Sheets sync
   ```
2. **Launch Stack**:
   ```bash
   docker compose up -d --build
   ```
3. **Verify Health**:
   - DB API: `http://localhost:8000/docs`
   - Logs: `docker compose logs -f gem6`

## 🛡️ Contract Violations
If an agent fails contract validation:
- GEM6 stops the flow.
- Check `discovery_logs` in the DB:
  ```sql
  SELECT * FROM discovery_logs WHERE status = 'CONTRACT_ERROR' ORDER BY created_at DESC;
  ```
- **Action**: Correct the `output_contract.json` or the agent's prompt/logic.

## 📉 Threshold & Drift
If `discard_rate` increases unexpectedly:
- Check `GEM2` scoring logs.
- Audit `discarded_entities` table to see if criteria is too strict.

## 💰 Cost & Resource Control
- **GEM6** enforces `max_tokens` (configure in environment).
- **Early Exit**: GEM2 scoring ensures we don't spend on low-quality entities.

## 🆘 Recovery
- **API Down**: `docker compose restart db-api`
- **DB Corruption**: Wipe `infra/db/gem_v3.sqlite` and restart (schema will auto-init).
