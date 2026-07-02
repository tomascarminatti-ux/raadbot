import pytest

@pytest.fixture(scope="module")
def server():
    import subprocess
    import time
    import os

    # Use a dummy GEMINI_API_KEY for testing
    env = os.environ.copy()
    env["GEMINI_API_KEY"] = "dummy_key"

    # Start the FastAPI server
    proc = subprocess.Popen(
        ["uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8001"],
        env=env
    )
    time.sleep(2)  # Wait for server to start
    yield "http://127.0.0.1:8001/dashboard"
    proc.terminate()

def test_dashboard_ux_elements(page, server):
    from playwright.sync_api import expect
    page.goto(server)

    # Check for ARIA labels on scrollable containers
    expect(page.locator("#gem-nav")).to_have_attribute("aria-label", "Navegación de módulos GEM")
    expect(page.locator("#gem-nav")).to_have_attribute("tabindex", "0")

    expect(page.locator("#prompt-content")).to_have_attribute("aria-label", "Contenido del System Prompt")
    expect(page.locator("#prompt-content")).to_have_attribute("tabindex", "0")

    expect(page.locator("#chat-history")).to_have_attribute("aria-label", "Historial de refinamiento")
    expect(page.locator("#chat-history")).to_have_attribute("tabindex", "0")

    # Check for ARIA labels on inputs
    expect(page.locator("#refine-input")).to_have_attribute("aria-label", "Instrucciones para refinar")
    expect(page.locator("#send-btn")).to_have_attribute("aria-label", "Refinar prompt")

    # Check for Copy button
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_disabled()
    expect(copy_btn).to_have_text("📋 Copiar")

def test_copy_to_clipboard(page, server, context):
    from playwright.sync_api import expect
    # Grant clipboard permissions
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto(server)

    # Wait for gems to load and select one
    # Note: selectGem might fail if the API call to /api/v1/gems fails because of dummy key
    # but the API.py doesn't actually call Gemini for listing gems.

    gem_btn = page.locator("#btn-gem1")
    gem_btn.click()

    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_enabled()

    # Click copy button
    copy_btn.click()

    # Check visual feedback
    expect(copy_btn).to_have_text("✅ ¡Copiado!")

    # Verify clipboard content
    # In some environments, reading from clipboard might be tricky
    # But let's try
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    prompt_content = page.locator("#prompt-content").inner_text()
    assert clipboard_text == prompt_content
