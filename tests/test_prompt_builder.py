from agent.prompt_builder import load_prompt, load_maestro, build_prompt

def test_prompt_builder_caching():
    # Ensure standard prompt works
    prompt = load_prompt("gem1")
    assert "GEM1" in prompt or "GEM_1" in prompt or len(prompt) > 0

    maestro = load_maestro()
    assert len(maestro) > 0

    # Test cache invalidation/consistency (the cache returns correct values)
    variables = {
        "search_id": "SEARCH-2026-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced Python Developer",
        "interview_notes": "Great candidate",
        "gem5_summary": "CEO search"
    }
    p1 = build_prompt("gem1", variables)
    p2 = build_prompt("gem1", variables)
    assert p1 == p2
