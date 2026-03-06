import pytest
import subprocess
import time
import os
import re
from playwright.sync_api import Page, expect


@pytest.fixture(scope="module", autouse=True)
def server():
    # Set dummy API key for testing
    os.environ["GEMINI_API_KEY"] = "dummy-key"
    # Start the server in the background
    proc = subprocess.Popen(["python", "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8000"])

    # Wait for server to start by polling
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            import httpx
            response = httpx.get("http://127.0.0.1:8000/health")
            if response.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(0.5)

    yield
    proc.terminate()


def test_dashboard_copy_button(page: Page):
    # Go to the dashboard
    page.goto("http://127.0.0.1:8000/dashboard")

    # Wait for the sidebar to load GEMS
    page.wait_for_selector("#gem-nav button")

    # Check that copy button is hidden initially
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_hidden()

    # Select the first GEM
    first_gem_btn = page.locator("#gem-nav button").first
    first_gem_btn.click()

    # Now the copy button should be visible
    expect(copy_btn).to_be_visible()
    expect(copy_btn).to_have_attribute("aria-label", "Copiar prompt al portapapeles")

    # Test accessibility: GEM buttons should have aria-label
    expect(first_gem_btn).to_have_attribute("aria-label", re.compile(r"Seleccionar GEM.*"))

    # Grant clipboard permissions
    page.context.grant_permissions(["clipboard-write", "clipboard-read"])

    # Click copy button
    copy_btn.click()

    # Check for "¡Copiado!" text
    expect(page.locator("#copy-text")).to_have_text("¡Copiado!")
    # Check class presence (border-green-500)
    expect(copy_btn).to_have_class(re.compile(r".*border-green-500.*"))

    # Wait for it to revert
    page.wait_for_timeout(2500)
    expect(page.locator("#copy-text")).to_have_text("Copiar")
    expect(copy_btn).not_to_have_class(re.compile(r".*border-green-500.*"))


def test_keyboard_navigation(page: Page):
    page.goto("http://127.0.0.1:8000/dashboard")
    page.wait_for_selector("#gem-nav button")

    # Focus the first GEM button
    page.focus("#gem-nav button:first-child")
    page.keyboard.press("Enter")

    # Tab to the copy button
    found = False
    for _ in range(15):
        page.keyboard.press("Tab")
        active_id = page.evaluate("document.activeElement.id")
        if active_id == "copy-btn":
            found = True
            break

    assert found, "Copy button should be reachable via keyboard"
