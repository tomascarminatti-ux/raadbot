from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_pipeline_run_path_traversal():
    """Test that path traversal in search_id is rejected."""
    response = client.post("/api/v1/run", json={
        "search_id": "../../etc/passwd",
        "local_dir": "."
    })
    assert response.status_code == 422
    assert "search_id" in response.text


def test_pipeline_run_valid_id():
    """Test that a valid search_id is accepted (even if it fails later due to missing API key)."""
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id_123",
        "local_dir": "."
    })
    # If API_KEY is missing, it returns 400. If it passes validation, it shouldn't be 422.
    assert response.status_code != 422


def test_search_setup_path_traversal():
    """Test that path traversal in search_id is rejected in search setup."""
    response = client.post("/api/v1/search/setup", json={
        "search_id": "invalid/path",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert response.status_code == 422


def test_gem_refine_invalid_gem():
    """Test that invalid gem_id is rejected."""
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem99",
        "instruction": "refine it"
    })
    assert response.status_code == 422


def test_gem_refine_valid_gem(mocker):
    """Test that valid gem_id is accepted."""
    # Mock GeminiClient.run_gem to avoid external API calls
    mocker.patch(
        "agent.gemini_client.GeminiClient.run_gem",
        return_value={"markdown": "new prompt", "raw": "new prompt", "json": None, "usage": {}}
    )

    # Mock the file system for prompts/gem1.md to avoid overwriting real files
    mocker.patch("os.path.exists", side_effect=lambda p: True if p == "prompts/gem1.md" else False)
    mock_open = mocker.mock_open(read_data="old prompt")
    mocker.patch("builtins.open", mock_open)

    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem1",
        "instruction": "refine it"
    })
    # Should not be 422.
    assert response.status_code != 422


def test_db_api_validation():
    """Test validation in DB API models (importing app from infra.db.api)."""
    from infra.db.api import app as db_app
    db_client = TestClient(db_app)

    # Test EntityUpdate validation
    response = db_client.post("/entity/upsert", json={
        "entity_id": "bad;id",
        "current_stage": "stage",
        "state": "state",
        "agent_responsible": "agent",
        "trace_id": "trace"
    })
    assert response.status_code == 422

    # Test DiscoveryLog validation
    response = db_client.post("/log/discovery", json={
        "entity_id": "valid",
        "agent_id": "invalid space",
        "input_ok": True,
        "output_ok": True,
        "time_ms": 100,
        "status": "ok",
        "trace_id": "trace"
    })
    assert response.status_code == 422
