import pytest
from fastapi.testclient import TestClient
from api import app
import os
import shutil

client = TestClient(app)

def test_path_traversal_search_id():
    # Attempt to create a directory outside of 'runs'
    search_id = "../traversal_test"
    # We need to provide either drive_folder or local_dir
    # local_dir = "." should be safe enough for this test
    response = client.post("/api/v1/run", json={
        "search_id": search_id,
        "local_dir": "."
    })

    # If successful, it would have created a directory 'traversal_test' in the root
    # (since os.path.join("runs", "../traversal_test", "outputs") -> "traversal_test/outputs")

    traversal_path = "traversal_test"
    exists = os.path.exists(traversal_path)

    if exists:
        shutil.rmtree(traversal_path)

    assert not exists, "Path traversal successful! Directory created outside of 'runs'."

def test_path_traversal_gem_id():
    # Attempt to read/write a file outside of 'prompts'
    # Since it appends .md, we try to target something that might exist or just check if it allows it
    gem_id = "../config" # targets config.py if it were to append .md? No, it appends .md
    # Let's try to target a file we create
    test_file = "prompts/../test_traversal.md"
    with open("test_traversal.md", "w") as f:
        f.write("secret")

    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../test_traversal",
        "instruction": "make it better"
    })

    # If it works, it might have overwritten or at least not failed with 404
    # But wait, the code does: prompt_path = f"prompts/{request.gem_id}.md"
    # prompts/../test_traversal.md -> test_traversal.md

    os.remove("test_traversal.md")

    # If we haven't fixed it, it might return 200 or 500 but not necessarily 400 validation error
    assert response.status_code != 200 or "status" in response.json() and response.json()["status"] == "error"
