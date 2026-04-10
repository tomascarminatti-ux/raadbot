import os

# Set dummy key before importing config/app to satisfy startup check
os.environ["GEMINI_API_KEY"] = "dummy_key"

import unittest
from fastapi.testclient import TestClient
import config

# Also set it in the config module directly in case it was already loaded
config.GEMINI_API_KEY = "dummy_key"

from api import app


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_path_traversal_search_id_run(self):
        payload = {
            "search_id": "../evil",
            "local_dir": "some/dir"
        }
        response = self.client.post("/api/v1/run", json=payload)
        assert response.status_code == 422
        assert "String should match pattern" in response.text

    def test_path_traversal_local_dir_run(self):
        payload = {
            "search_id": "valid_id",
            "local_dir": "/etc/passwd"
        }
        response = self.client.post("/api/v1/run", json=payload)
        assert response.status_code == 422
        assert "local_dir must be a relative path" in response.text

    def test_path_traversal_search_id_setup(self):
        payload = {
            "search_id": "invalid/id",
            "brief_notes": "notes",
            "jd_content": "jd"
        }
        response = self.client.post("/api/v1/search/setup", json=payload)
        assert response.status_code == 422

    def test_path_traversal_gem_id_refine(self):
        payload = {
            "gem_id": "gem1; rm -rf /",
            "instruction": "refine"
        }
        response = self.client.post("/api/v1/gems/refine", json=payload)
        assert response.status_code == 422

    def test_valid_inputs(self):
        # This should PASS Pydantic validation (not 422)
        payload = {
            "search_id": "valid-search_123",
            "local_dir": "relative/path"
        }
        response = self.client.post("/api/v1/run", json=payload)
        # If it's not 422, it's valid according to Pydantic
        assert response.status_code != 422

if __name__ == "__main__":
    unittest.main()
