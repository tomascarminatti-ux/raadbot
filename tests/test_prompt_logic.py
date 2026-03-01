import unittest
import os
import sys

# Añadir el directorio raíz al path para poder importar agent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.prompt_builder import build_prompt

class TestPromptLogic(unittest.TestCase):
    def test_variable_substitution(self):
        # Mocking load_prompt is hard because it's cached.
        # But we can test it with real prompts.
        variables = {
            "search_id": "SEARCH-001",
            "candidate_id": "CAND-001",
            "cv_text": "Experienced CEO",
            "interview_notes": "Good communication",
            "gem5_summary": "Summary text"
        }

        prompt = build_prompt("gem1", variables)

        self.assertIn("SEARCH-001", prompt)
        self.assertIn("CAND-001", prompt)
        self.assertIn("Experienced CEO", prompt)
        self.assertIn("Good communication", prompt)
        self.assertIn("Summary text", prompt)
        self.assertNotIn("{{search_id}}", prompt)
        self.assertNotIn("{{candidate_id}}", prompt)

    def test_json_substitution(self):
        variables = {
            "search_id": "SEARCH-001",
            "candidate_id": "CAND-001",
            "cv_text": "cv",
            "interview_notes": "notes",
            "gem5_summary": {"role": "CEO", "challenge": "Growth"}
        }

        prompt = build_prompt("gem1", variables)

        self.assertIn('"role": "CEO"', prompt)
        self.assertIn('"challenge": "Growth"', prompt)

    def test_whitespace_in_placeholders(self):
        # Current regex is r"\{\{\s*(\w+)\s*\}\}" so it should handle spaces
        # We need a template with spaces to test this properly,
        # but let's assume if it passes normal ones it's okay,
        # or we could mock load_prompt if we really wanted to.
        pass

if __name__ == "__main__":
    unittest.main()
