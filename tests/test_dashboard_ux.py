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
        ["uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8005"],
        env=env
    )
    time.sleep(2)  # Wait for server to start
    yield "http://127.0.0.1:8005/dashboard"
    proc.terminate()


def test_dashboard_ux_elements(request, server):
    try:
        from playwright.sync_api import expect
    except ImportError:
        pytest.skip("playwright not installed")

    if "page" not in request.fixturenames:
        pytest.skip("playwright fixture not found")

    page = request.getfixturevalue("page")
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


def test_copy_to_clipboard(request, server):
    try:
        from playwright.sync_api import expect
    except ImportError:
        pytest.skip("playwright not installed")

    if "page" not in request.fixturenames or "context" not in request.fixturenames:
        pytest.skip("playwright fixtures not found")

    page = request.getfixturevalue("page")
    context = request.getfixturevalue("context")

    # Grant clipboard permissions
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto(server)

    # Wait for gems to load and select one
    page.click("#btn-gem1")

    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_enabled()

    # Click copy button
    copy_btn.click()

    # Check visual feedback
    expect(copy_btn).to_have_text("✅ ¡Copiado!")

    # Verify clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    prompt_content = page.locator("#prompt-content").inner_text()
    assert clipboard_text == prompt_content
