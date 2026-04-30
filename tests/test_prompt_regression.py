import unittest
import os
import sys

# Ensure agent package is findable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.prompt_builder import build_prompt

class TestPromptRegression(unittest.TestCase):
    def test_build_prompt_basic(self):
        variables = {"search_id": "TEST-123"}
        # gem5 uses {{search_id}}
        prompt = build_prompt("gem5", variables)
        self.assertIn("TEST-123", prompt)
        self.assertNotIn("{{search_id}}", prompt)
        # Check if maestro is injected by checking for a known section
        self.assertIn("[NON-NEGOTIABLE RULES]", prompt)

    def test_build_prompt_json_var(self):
        variables = {"search_id": "ID", "candidate_id": "CID", "cv_text": "CV", "interview_notes": "IN", "gem5_summary": {"data": 1}}
        try:
            prompt = build_prompt("gem1", variables)
            self.assertIn('"data": 1', prompt)
        except Exception as e:
            self.fail(f"build_prompt failed with dict variable: {e}")

if __name__ == "__main__":
    unittest.main()
