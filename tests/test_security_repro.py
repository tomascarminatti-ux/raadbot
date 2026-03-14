import unittest
from fastapi.testclient import TestClient
import os
import sys

# Add root to path to import api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app

client = TestClient(app)

class TestSecurity(unittest.TestCase):
    def test_path_traversal_search_id(self):
        # Attempt to create a directory outside of 'runs'
        payload = {
            "search_id": "../evil_dir",
            "local_dir": "."
        }
        response = client.post("/api/v1/run", json=payload)
        # It might still fail because of other reasons (like GEMINI_API_KEY missing),
        # but we want to see if 'evil_dir' was created in the root.
        self.assertFalse(os.path.exists("evil_dir"))
        if os.path.exists("../evil_dir"): # In case it's relative to runs/
             os.rmdir("../evil_dir")
             self.fail("Path traversal successful in search_id!")

    def test_path_traversal_gem_id(self):
        # Attempt to read a file outside prompts
        payload = {
            "gem_id": "../config",
            "instruction": "test"
        }
        response = client.post("/api/v1/gems/refine", json=payload)
        # If it returns 404 with "GEM prompt file not found", it might be because it appended .md
        # But we want to ensure it doesn't even try to look there.
        # More importantly, if we use a valid file but outside prompts:
        # Let's say we have README.md in root. gem_id = "../README"
        payload = {
            "gem_id": "../README",
            "instruction": "test"
        }
        response = client.post("/api/v1/gems/refine", json=payload)
        self.assertNotEqual(response.status_code, 200)

if __name__ == "__main__":
    # Ensure runs exists
    os.makedirs("runs", exist_ok=True)
    unittest.main()
