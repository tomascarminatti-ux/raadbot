import unittest
import os
from agent.prompt_builder import build_prompt

class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        # Create prompts directory and mock prompts
        os.makedirs("prompts", exist_ok=True)
        with open("prompts/00_prompt_maestro.md", "w") as f:
            f.write("Maestro")
        with open("prompts/test_gem.md", "w") as f:
            f.write("GEM: {{PROMPT_MAESTRO}} {{var1}} {{var2}}")

    def test_build_prompt(self):
        variables = {"var1": "value1", "var2": {"nested": "value2"}}
        prompt = build_prompt("test_gem", variables)
        self.assertIn("Maestro", prompt)
        self.assertIn("value1", prompt)
        self.assertIn('"nested": "value2"', prompt)
        self.assertNotIn("{{var1}}", prompt)
        self.assertNotIn("{{PROMPT_MAESTRO}}", prompt)

    def test_build_prompt_missing_var(self):
        variables = {"var1": "value1"}
        # This should print a warning but return the prompt with remaining placeholders
        prompt = build_prompt("test_gem", variables)
        self.assertIn("{{var2}}", prompt)

if __name__ == "__main__":
    unittest.main()
