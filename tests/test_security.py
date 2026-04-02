import unittest
from fastapi.testclient import TestClient
import os
import socket

# Set dummy API key to bypass startup check
os.environ["GEMINI_API_KEY"] = "dummy"

from api import app

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_path_traversal_refine_gem(self):
        # gem_id with directory traversal characters should fail Pydantic validation
        response = self.client.post("/api/v1/gems/refine", json={
            "gem_id": "../api",
            "instruction": "Just a test"
        })
        self.assertEqual(response.status_code, 422) # Unprocessable Entity due to pattern mismatch
        self.assertIn("string_pattern_mismatch", response.text)

    def test_path_traversal_search_id(self):
        response = self.client.post("/api/v1/search/setup", json={
            "search_id": "test/../../malicious",
            "brief_notes": "notes",
            "jd_content": "jd"
        })
        self.assertEqual(response.status_code, 422)
        self.assertIn("string_pattern_mismatch", response.text)

    def test_local_dir_traversal(self):
        response = self.client.post("/api/v1/run", json={
            "search_id": "test-search",
            "local_dir": "/etc/passwd",
            "webhook_url": "https://example.com/webhook"
        })
        self.assertEqual(response.status_code, 422)
        self.assertIn("local_dir must be a relative path", response.text)

        response = self.client.post("/api/v1/run", json={
            "search_id": "test-search",
            "local_dir": "runs/../config",
            "webhook_url": "https://example.com/webhook"
        })
        self.assertEqual(response.status_code, 422)
        self.assertIn("cannot contain '..'", response.text)

    def test_ssrf_protection_loopback(self):
        response = self.client.post("/api/v1/run", json={
            "search_id": "test-search",
            "local_dir": "runs",
            "webhook_url": "http://127.0.0.1:8000/health"
        })
        self.assertEqual(response.status_code, 422)
        self.assertIn("is a private or loopback address", response.text)

    def test_ssrf_protection_private_ip(self):
        response = self.client.post("/api/v1/run", json={
            "search_id": "test-search",
            "local_dir": "runs",
            "webhook_url": "http://192.168.1.1/webhook"
        })
        self.assertEqual(response.status_code, 422)
        self.assertIn("is a private or loopback address", response.text)

    def test_ssrf_protection_localhost_domain(self):
        response = self.client.post("/api/v1/run", json={
            "search_id": "test-search",
            "local_dir": "runs",
            "webhook_url": "http://localhost:8000/health"
        })
        self.assertEqual(response.status_code, 422)
        self.assertIn("is a private or loopback address", response.text)

    def test_valid_request(self):
        # Valid search_id and webhook_url should pass validation
        # (It will fail later because of missing files or real GEMINI_API_KEY, but should pass Pydantic)
        response = self.client.post("/api/v1/run", json={
            "search_id": "valid-id_123",
            "local_dir": "runs",
            "webhook_url": "https://webhook.site/valid-path"
        })
        # If it passes Pydantic, it should proceed to run_pipeline and likely fail there
        # with a 400 or ValueError about missing inputs, NOT 422.
        self.assertNotEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
