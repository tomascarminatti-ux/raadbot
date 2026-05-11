import unittest
from agent.prompt_builder import build_prompt, load_prompt, load_maestro

class TestPromptBuilder(unittest.TestCase):
    def test_build_prompt_basic(self):
        variables = {
            "search_id": "test_search",
            "candidate_id": "CAND-001",
            "cv_text": "Experienced software engineer",
            "interview_notes": "Good communication",
            "gem5_summary": "Summary"
        }
        prompt = build_prompt("gem1", variables)
        self.assertIn("test_search", prompt)
        self.assertIn("CAND-001", prompt)
        self.assertIn("Experienced software engineer", prompt)
        # Check if maestro was injected
        self.assertIn("[ROLE]", prompt)
        self.assertIn("Consultor Senior de Executive Search", prompt)

    def test_build_prompt_with_dict(self):
        variables = {
            "search_id": "test_search",
            "complex_var": {"key": "value"}
        }
        # gem1 might not have complex_var, but build_prompt should still work
        prompt = build_prompt("gem1", variables)
        self.assertIn("test_search", prompt)

    def test_caching(self):
        # Initial calls
        p1 = load_prompt("gem1")
        m1 = load_maestro()

        # Subsequent calls should return the same object if it was the same string
        # though strings might be interned or not, but content must be same
        p2 = load_prompt("gem1")
        m2 = load_maestro()

        self.assertEqual(p1, p2)
        self.assertEqual(m1, m2)

if __name__ == "__main__":
    unittest.main()
