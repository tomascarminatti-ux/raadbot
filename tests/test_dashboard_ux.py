import pytest
from playwright.sync_api import Page, expect
import threading
import uvicorn
import time
import re
from api import app

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001)

@pytest.fixture(scope="module", autouse=True)
def server():
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(2)  # Wait for server to start
    yield

def test_dashboard_ux_elements(page: Page):
    page.goto("http://127.0.0.1:8001/dashboard")

    # Check Spanish localization
    expect(page.get_by_text("Solo lectura")).to_be_visible()

    # Check for gems in nav and select one
    # We might need to wait for gems to load
    page.wait_for_selector("#gem-nav button")
    gem_btn = page.locator("#gem-nav button").first
    gem_btn.click()

    # Check if copy button appears
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_visible()
    expect(copy_btn).to_have_attribute("aria-label", "Copiar prompt al portapapeles")

    # Verify focus visible class is present
    expect(gem_btn).to_have_class(re.compile(".*focus-visible:ring-2.*"))

    # Click copy button and check visual feedback
    # Note: navigator.clipboard might require a secure context or specific permissions in playwright
    # but we can at least check if the UI reacts.
    copy_btn.click(force=True)
    page.wait_for_selector("#copy-text:has-text('Copiado')")
    expect(page.locator("#copy-text")).to_have_text("Copiado")

    # Wait for reset or select another gem to check reset
    if page.locator("#gem-nav button").count() > 1:
        second_gem_btn = page.locator("#gem-nav button").nth(1)
        second_gem_btn.click()
        expect(page.get_by_text("Copiar")).to_be_visible()
        expect(page.get_by_text("Copiado")).not_to_be_visible()
