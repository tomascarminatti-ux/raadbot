import unittest
import os
import tempfile
import shutil
from agent import prompt_builder
from agent.prompt_builder import build_prompt


class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.original_dir = prompt_builder.PROMPTS_DIR
        prompt_builder.PROMPTS_DIR = self.tmp_dir
        prompt_builder.load_prompt.cache_clear()

        with open(os.path.join(self.tmp_dir, "00_prompt_maestro.md"), "w") as f:
            f.write("Maestro: {{var1}}")
        with open(os.path.join(self.tmp_dir, "test_gem.md"), "w") as f:
            f.write("Gem: {{PROMPT_MAESTRO}}, {{var2}}")

    def tearDown(self):
        prompt_builder.PROMPTS_DIR = self.original_dir
        prompt_builder.load_prompt.cache_clear()
        shutil.rmtree(self.tmp_dir)

    def test_build_prompt(self):
        variables = {"var1": "V1", "var2": "V2"}
        result = build_prompt("test_gem", variables)
        self.assertEqual(result, "Gem: Maestro: V1, V2")

    def test_json_variable(self):
        variables = {"var1": "V1", "var2": {"key": "val"}}
        result = build_prompt("test_gem", variables)
        self.assertIn('"key": "val"', result)

    def test_missing_variable(self):
        variables = {"var1": "V1"}
        result = build_prompt("test_gem", variables)
        self.assertIn("{{var2}}", result)


if __name__ == "__main__":
    unittest.main()
