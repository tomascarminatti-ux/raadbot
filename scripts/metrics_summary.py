import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "infra/db/gem_v3.sqlite")

QUERIES = {
    "results_per_query": """
        SELECT agent_id, COUNT(*) as count 
        FROM discovery_logs 
        GROUP BY agent_id
    """,
    "discard_rate": """
        SELECT 
            (SELECT COUNT(*) FROM discarded_entities) * 1.0 / 
            ((SELECT COUNT(*) FROM entity_state) + (SELECT COUNT(*) FROM discarded_entities)) as rate
    """,
    "acceptance_rate": """
        SELECT 
            COUNT(*) * 1.0 / (SELECT COUNT(*) FROM discovery_logs WHERE agent_id = 'GEM3')
        FROM entity_state 
        WHERE current_stage = 'COMPLETED'
    """,
    "avg_processing_time": """
        SELECT agent_id, AVG(execution_time_ms) as avg_time 
        FROM discovery_logs 
        GROUP BY agent_id
    """,
    "funnel_counts": """
        SELECT current_stage, COUNT(*) as count 
        FROM entity_state 
        GROUP BY current_stage
    """
}

def print_metrics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("--- GEM v3.0 FUNNEL METRICS ---")
    for name, query in QUERIES.items():
        print(f"\nMetric: {name}")
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    conn.close()

if __name__ == "__main__":
    print_metrics()
