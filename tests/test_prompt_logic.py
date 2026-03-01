import os
import sys
import unittest

# Ensure we can import from the root
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

class TestPromptBuilder(unittest.TestCase):
    def test_nested_variables(self):
        # Injecting a variable that is only inside the Maestro
        from agent import prompt_builder
        import os

        maestro_content = "This is maestro version {{VERSION}}"
        gem_content = "{{PROMPT_MAESTRO}}\nThis is gem {{GEM_ID}}"

        # Mock load_prompt to return our test strings
        original_load_prompt = prompt_builder.load_prompt

        from unittest.mock import MagicMock
        mock_lp = MagicMock(side_effect=lambda name: maestro_content if name == "00_prompt_maestro" else gem_content)
        prompt_builder.load_prompt = mock_lp

        try:
            variables = {"VERSION": "1.2.3", "GEM_ID": "GEM-ABC"}
            prompt = build_prompt("some_gem", variables)

            self.assertIn("This is maestro version 1.2.3", prompt)
            self.assertIn("This is gem GEM-ABC", prompt)
        finally:
            prompt_builder.load_prompt = original_load_prompt

    def test_basic_substitution(self):
        # Gem 6 doesn't have {{search_id}} or {{context}} in the template file,
        # but build_agent_prompt (which uses build_prompt) appends payload if placeholders are missing.
        from agent.prompt_builder import build_agent_prompt
        payload = {"search_id": "123", "context": "MY_CONTEXT"}
        prompt = build_agent_prompt("gem6", payload)
        self.assertIn("MY_CONTEXT", prompt)
        self.assertIn("123", prompt)

if __name__ == "__main__":
    unittest.main()
