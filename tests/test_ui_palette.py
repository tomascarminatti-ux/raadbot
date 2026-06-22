import pytest
import multiprocessing
import time
import uvicorn
import httpx
try:
    from playwright.sync_api import Page, expect
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

def run_server():
    from api import app
    import config
    # Ensure a dummy API key for testing if not present
    if not config.GEMINI_API_KEY:
        config.GEMINI_API_KEY = "dummy_key"
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

@pytest.fixture(scope="module", autouse=True)
def server():
    proc = multiprocessing.Process(target=run_server, daemon=True)
    proc.start()

    # Wait for server to be ready
    timeout = 15
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = httpx.get("http://127.0.0.1:8001/health")
            if response.status_code == 200:
                print("Server is up!")
                break
        except httpx.RequestError:
            pass
        time.sleep(1)
    else:
        proc.terminate()
        pytest.fail("Server failed to start")

    yield
    proc.terminate()

@pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright not installed")
def test_dashboard_copy_button(page: Page):
    # Navigate to dashboard
    page.goto("http://127.0.0.1:8001/dashboard")

    # Check initial state
    expect(page.get_by_text("Selecciona un Módulo GEM")).to_be_visible()

    # Copy button should be hidden initially
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_hidden()

    # Click a GEM button in the sidebar (wait for it to load)
    # The first GEM should be GEM1
    gem_btn = page.get_by_role("button", name="Seleccionar GEM1")
    gem_btn.wait_for(state="visible", timeout=10000)
    gem_btn.click()

    # Copy button should now be visible
    expect(copy_btn).to_be_visible()
    expect(page.locator("#current-gem-title")).to_contain_text("GEM1")

    # Mock clipboard
    page.evaluate("navigator.clipboard.writeText = (text) => { window.lastCopiedText = text; return Promise.resolve(); }")

    # Click copy button
    copy_btn.click()

    # Verify visual feedback
    expect(page.locator("#copy-text")).to_have_text("¡Copiado!")
    expect(page.locator("#copy-icon")).to_have_text("✅")

    # Wait for feedback to reset
    page.wait_for_timeout(2500)
    expect(page.locator("#copy-text")).to_have_text("Copiar")
    expect(page.locator("#copy-icon")).to_have_text("📋")

@pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright not installed")
def test_accessibility_attributes(page: Page):
    page.goto("http://127.0.0.1:8001/dashboard")

    # Check ARIA labels
    expect(page.locator("#refine-input")).to_have_attribute("aria-label", "Instrucciones de refinamiento")
    expect(page.locator("#send-btn")).to_have_attribute("aria-label", "Enviar refinamiento")

    # Wait for gems and check their buttons
    gem_btn = page.get_by_role("button", name="Seleccionar GEM1")
    gem_btn.wait_for(state="visible", timeout=10000)
    expect(gem_btn).to_have_attribute("aria-label", "Seleccionar GEM1")
