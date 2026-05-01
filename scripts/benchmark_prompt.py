import time
import os
import sys
import tempfile
import shutil

# Añadir el directorio raíz al path para poder importar agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt
from agent import prompt_builder


def benchmark_build_prompt():
    variables = {
        "var1": "value1",
        "var2": "value2",
        "var3": {"nested": "value3"},
        "var4": "value4",
        "var5": "value5",
    }

    tmp_dir = tempfile.mkdtemp()
    original_dir = prompt_builder.PROMPTS_DIR
    prompt_builder.PROMPTS_DIR = tmp_dir
    prompt_builder.load_prompt.cache_clear()

    try:
        with open(os.path.join(tmp_dir, "00_prompt_maestro.md"), "w") as f:
            f.write("Maestro content with {{var1}}")
        with open(os.path.join(tmp_dir, "benchmark_gem.md"), "w") as f:
            f.write("Gem content with {{PROMPT_MAESTRO}}, {{var2}}, {{var3}}, {{var4}}, {{var5}} and {{VERSION}}")

        # Warmup
        for _ in range(100):
            build_prompt("benchmark_gem", variables)

        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            build_prompt("benchmark_gem", variables)
        end_time = time.time()

        avg_time = (end_time - start_time) / iterations
        print(f"Average time for build_prompt: {avg_time*1000:.4f} ms")

    finally:
        prompt_builder.PROMPTS_DIR = original_dir
        prompt_builder.load_prompt.cache_clear()
        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    benchmark_build_prompt()
