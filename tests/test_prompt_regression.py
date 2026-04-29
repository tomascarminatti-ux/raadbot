import os
import sys
import traceback

# Add project root to sys.path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def test_build_prompt_replacement():
    # Setup test variables
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-456",
        "cv_text": "Sample CV",
        "interview_notes": "Sample Interview Notes",
        "gem5_summary": "Sample GEM5 Summary",
        "custom_var": {"key": "value"}
    }

    # Run build_prompt for gem1
    prompt = build_prompt("gem1", variables)

    # Assertions
    # 1. Maestro is injected
    assert "Eres Consultor Senior de Executive Search en RAAD" in prompt

    # 2. Basic variables are replaced
    assert "SEARCH-123" in prompt
    assert "CAND-456" in prompt
    assert "Sample CV" in prompt

    # 3. Verification of no remaining variables
    import re
    remaining = re.findall(r"\{\{(\w+)\}\}", prompt)
    remaining = [v for v in remaining if v != "VERSION"]
    assert len(remaining) == 0, f"Unreplaced variables found: {remaining}"

if __name__ == "__main__":
    try:
        test_build_prompt_replacement()
        print("✅ Regression test passed!")
    except Exception:
        print("❌ Regression test failed:")
        traceback.print_exc()
        sys.exit(1)
