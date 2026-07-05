
import unittest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch

# Set dummy environment variables before importing app
os.environ["GEMINI_API_KEY"] = "dummy_key"
os.environ["LLM_PROVIDER"] = "gemini"

from api import app

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_path_traversal_search_id_setup(self):
        # Setup should fail with 422 if search_id contains dots or slashes
        payloads = [
            {"search_id": "../exploit", "brief_notes": "t", "jd_content": "t"},
            {"search_id": "sub/dir", "brief_notes": "t", "jd_content": "t"},
            {"search_id": "/abs/path", "brief_notes": "t", "jd_content": "t"},
        ]
        for payload in payloads:
            response = self.client.post("/api/v1/search/setup", json=payload)
            self.assertEqual(response.status_code, 422, f"Failed for {payload['search_id']}")

    def test_path_traversal_local_dir_run(self):
        # Run should fail with 422 if local_dir is absolute or contains ..
        payloads = [
            {"search_id": "valid", "local_dir": "/etc"},
            {"search_id": "valid", "local_dir": "valid/../../etc"},
            {"search_id": "valid", "local_dir": "../direct"},
        ]
        for payload in payloads:
            response = self.client.post("/api/v1/run", json=payload)
            self.assertEqual(response.status_code, 422, f"Failed for {payload['local_dir']}")

    def test_path_traversal_gem_id_refine(self):
        # Refine should fail with 422 if gem_id contains dots or slashes
        payloads = [
            {"gem_id": "../config", "instruction": "t"},
            {"gem_id": "prompts/gem1", "instruction": "t"},
        ]
        for payload in payloads:
            response = self.client.post("/api/v1/gems/refine", json=payload)
            self.assertEqual(response.status_code, 422, f"Failed for {payload['gem_id']}")

    def test_valid_inputs(self):
        # Valid inputs should NOT return 422 (might return 400 or something else due to missing mocks/files, but not validation error)
        payload = {"search_id": "valid-id_123", "brief_notes": "t", "jd_content": "t"}
        with patch("agent.gemini_client.GeminiClient.run_gem") as mock_run:
            mock_run.return_value = {"data": {}, "markdown": ""}
            response = self.client.post("/api/v1/search/setup", json=payload)
            self.assertNotEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
