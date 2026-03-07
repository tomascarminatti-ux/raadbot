import pytest
import re
import httpx
from playwright.sync_api import expect
import time


def wait_for_server(url, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = httpx.get(f"{url}/health")
            if response.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def test_dashboard_accessibility_and_copy(page):
    # Wait for server to be ready
    server_ready = wait_for_server("http://127.0.0.1:8000")
    if not server_ready:
        pytest.fail("Server failed to start")

    # Grant clipboard permissions for 127.0.0.1
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"], origin="http://127.0.0.1:8000")

    page.goto("http://127.0.0.1:8000/dashboard", wait_until="networkidle")

    # Check for sidebar button accessibility
    page.wait_for_selector("#gem-nav button")

    first_gem_btn = page.locator("#gem-nav button").first
    expect(first_gem_btn).to_have_attribute("aria-label", re.compile(r"Seleccionar GEM\d"))

    # Verify Copy button is hidden initially
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_hidden()

    # Select a GEM
    first_gem_btn.click()

    # Verify Copy button is revealed
    expect(copy_btn).to_be_visible()
    expect(copy_btn).to_have_attribute("aria-label", "Copiar System Prompt")

    # Test copy functionality feedback
    # We click and expect it to change
    copy_btn.click()

    copy_text = page.locator("#copy-text")
    expect(copy_text).to_have_text("¡Copiado!", timeout=10000)

    # Check if it reverts after some time
    page.wait_for_timeout(3000)
    expect(copy_text).to_have_text("Copiar")


if __name__ == "__main__":
    pass
