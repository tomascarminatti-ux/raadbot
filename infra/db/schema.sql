-- GEM v3.0 Industrial Schema

-- Table for tracking entities and their current state in the funnel
CREATE TABLE IF NOT EXISTS entity_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT UNIQUE NOT NULL,
    current_stage TEXT NOT NULL, -- GEM1, GEM2, GEM3, GEM4, COMPLETED
    state TEXT NOT NULL, -- PENDING, PROCESSING, COMPLETED, REJECTED, FAILED
    last_score REAL,
    human_required BOOLEAN DEFAULT 0,
    metadata JSON,
    agent_responsible TEXT,
    trace_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for discarded entities (Audit Trail)
CREATE TABLE IF NOT EXISTS discarded_entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL,
    stage_at_discard TEXT NOT NULL,
    reason TEXT,
    score_at_discard REAL,
    metadata JSON,
    agent_responsible TEXT,
    trace_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Detailed logs per agent execution
CREATE TABLE IF NOT EXISTS discovery_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    input_contract_verified BOOLEAN,
    output_contract_verified BOOLEAN,
    execution_time_ms INTEGER,
    status TEXT,
    error_message TEXT,
    trace_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance and Funnel metrics
CREATE TABLE IF NOT EXISTS performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    dimensions JSON, -- e.g. {"agent": "GEM2", "date": "2024-03-20"}
    trace_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_entity_state_entity_id ON entity_state(entity_id);
CREATE INDEX IF NOT EXISTS idx_entity_state_state ON entity_state(state);
CREATE INDEX IF NOT EXISTS idx_discovery_logs_entity_id ON discovery_logs(entity_id);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_name ON performance_metrics(metric_name);
