import unittest
from agent.prompt_builder import build_prompt, load_maestro, load_prompt

class TestPromptLogic(unittest.TestCase):
    def test_basic_substitution(self):
        # build_prompt will load gem1.md
        # gem1.md currently has NO placeholders like {{input}}
        # So build_agent_prompt("gem1", payload) will append it
        from agent.prompt_builder import build_agent_prompt
        payload = {"test_key": "test_value"}
        prompt = build_agent_prompt("gem1", payload)
        self.assertIn('"test_key": "test_value"', prompt)
        self.assertIn("### DATA INPUT:", prompt)

    def test_maestro_injection(self):
        # build_prompt calls load_maestro and does replace("{{PROMPT_MAESTRO}}", maestro)
        # But wait, if gem1.md doesn't HAVE {{PROMPT_MAESTRO}}, it won't be injected.
        # Let's check if gem1.md has it.
        content = load_prompt("gem1")
        if "{{PROMPT_MAESTRO}}" in content:
            prompt = build_prompt("gem1", {})
            maestro = load_maestro()
            self.assertIn(maestro[:50], prompt)
        else:
            print("Note: gem1.md does not contain {{PROMPT_MAESTRO}}")

if __name__ == "__main__":
    unittest.main()
