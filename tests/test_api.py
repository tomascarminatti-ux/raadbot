import pytest
from fastapi.testclient import TestClient
import os
from unittest.mock import patch

# Set dummy API key for tests
os.environ["GEMINI_API_KEY"] = "test-key"

from api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "agent": "raadbot"}

def test_trigger_pipeline_missing_inputs():
    response = client.post("/api/v1/run", json={"search_id": "TEST"})
    assert response.status_code == 400
    assert "Se debe proveer" in response.json()["detail"]

def test_trigger_pipeline_invalid_local_dir():
    response = client.post("/api/v1/run", json={"search_id": "TEST", "local_dir": "/non/existent"})
    assert response.status_code == 400
    assert "Error cargando directorio local" in response.json()["detail"]
