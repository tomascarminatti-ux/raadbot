
import os
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_setup_search():
    # Attempt to create a directory outside of 'runs'
    traversal_id = "../../evil_search"
    response = client.post("/api/v1/search/setup", json={
        "search_id": traversal_id,
        "brief_notes": "test",
        "jd_content": "test"
    })

    # Even if it fails due to missing GEMINI_API_KEY, check if directory was created
    # But wait, it might fail before creating the directory or after.
    # In api.py:
    # output_dir = os.path.join("runs", request.search_id, "outputs")
    # os.makedirs(output_dir, exist_ok=True)

    evil_path = os.path.join("evil_search", "outputs")
    exists = os.path.exists(evil_path)

    # Cleanup if it was created
    if exists:
        import shutil
        shutil.rmtree("evil_search")

    assert not exists, "Path traversal vulnerability: directory created outside of 'runs'"

def test_path_traversal_refine_gem():
    # Attempt to read a file outside of 'prompts'
    # Actually refine_gem does f"prompts/{request.gem_id}.md"
    # So we need a .md file outside.

    # Create a dummy .md file in the root
    with open("secret.md", "w") as f:
        f.write("sensitive data")

    traversal_id = "../secret" # will become prompts/../secret.md -> secret.md

    response = client.post("/api/v1/gems/refine", json={
        "gem_id": traversal_id,
        "instruction": "refine"
    })

    # If vulnerable, it might try to read secret.md and then call Gemini.
    # We can check if it returned 404 or something else.
    # If it's NOT vulnerable (e.g. if we add validation), it should return 422 or 400.

    os.remove("secret.md")

    # If the file was found, it continues to GeminiClient(api_key=config.GEMINI_API_KEY)
    # If GEMINI_API_KEY is not set, it might raise an error.

    assert response.status_code != 200 # Should not be successful with traversal
