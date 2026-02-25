
import pytest
import os
from unittest.mock import patch, mock_open
from agent.prompt_builder import load_prompt, build_prompt, clear_prompt_caches

def test_load_prompt_caching():
    # Clear cache before test
    clear_prompt_caches()

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="template content")) as mocked_file:
            # First call should read from disk
            content1 = load_prompt("test_gem")
            assert content1 == "template content"
            mocked_file.assert_called_once()

            # Second call should read from cache
            content2 = load_prompt("test_gem")
            assert content2 == "template content"
            # still called once
            mocked_file.assert_called_once()

def test_build_prompt_injection():
    with patch("agent.prompt_builder.load_maestro", return_value="MAESTRO with {{var1}}"):
        with patch("agent.prompt_builder.load_prompt", return_value="GEM with {{PROMPT_MAESTRO}}"):
            variables = {"var1": "VALUE1"}
            result = build_prompt("test_gem", variables)

            assert "VALUE1" in result
            assert "MAESTRO with VALUE1" in result
            assert "{{var1}}" not in result
            assert "{{PROMPT_MAESTRO}}" not in result

def test_build_prompt_json_serialization():
    with patch("agent.prompt_builder.load_maestro", return_value="MAESTRO"):
        with patch("agent.prompt_builder.load_prompt", return_value="Data: {{data}}"):
            variables = {"data": {"key": "value"}}
            result = build_prompt("test_gem", variables)

            assert '"key": "value"' in result
            assert "Data: {" in result

def test_build_prompt_missing_variable():
    with patch("agent.prompt_builder.load_maestro", return_value="MAESTRO"):
        with patch("agent.prompt_builder.load_prompt", return_value="Need {{missing}}"):
            # Should keep the placeholder if missing
            result = build_prompt("test_gem", {})
            assert "Need {{missing}}" in result

def test_clear_prompt_caches():
    clear_prompt_caches()
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="content")) as mocked_file:
            load_prompt("test_gem_new")
            mocked_file.assert_called_once()

            clear_prompt_caches()
            load_prompt("test_gem_new")
            # Should be called again after clear
            assert mocked_file.call_count == 2
