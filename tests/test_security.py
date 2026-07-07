import unittest
import os
from fastapi.testclient import TestClient

# Set dummy API key for testing
os.environ["GEMINI_API_KEY"] = "dummy_key"

from api import app

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_path_traversal_search_id_pydantic(self):
        # search_id with dots should be rejected by Pydantic pattern
        response = self.client.post(
            "/api/v1/run",
            json={
                "search_id": "../../evil",
                "local_dir": "."
            }
        )
        self.assertEqual(response.status_code, 422)

    def test_path_traversal_local_dir_pydantic(self):
        # absolute path in local_dir should be rejected by field_validator
        response = self.client.post(
            "/api/v1/run",
            json={
                "search_id": "valid_id",
                "local_dir": "/etc"
            }
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("local_dir must be a relative path", response.text)

    def test_path_traversal_local_dir_dots_pydantic(self):
        # '..' in local_dir should be rejected by field_validator
        response = self.client.post(
            "/api/v1/run",
            json={
                "search_id": "valid_id",
                "local_dir": "../secrets"
            }
        )
        self.assertEqual(response.status_code, 422)

    def test_path_traversal_gem_id_pydantic(self):
        # gem_id with slashes should be rejected by Pydantic pattern
        response = self.client.post(
            "/api/v1/gems/refine",
            json={
                "gem_id": "sub/folder",
                "instruction": "test"
            }
        )
        self.assertEqual(response.status_code, 422)

    def test_path_traversal_setup_search_pydantic(self):
        # setup_search search_id validation
        response = self.client.post(
            "/api/v1/search/setup",
            json={
                "search_id": "invalid.id",
                "brief_notes": "notes",
                "jd_content": "jd"
            }
        )
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
