import pytest
import re
import time
import subprocess
import os

# Try to import playwright, if not available, tests will be skipped
try:
    from playwright.sync_api import Page, expect
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# Helper to start/stop the server
@pytest.fixture(scope="module", autouse=True)
def server():
    # Start server
    proc = subprocess.Popen(
        ["python3", "-m", "uvicorn", "api:app", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Wait for server to be ready
    time.sleep(3)
    yield
    proc.terminate()

@pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright not installed")
def test_dashboard_copy_button_exists(page):
    page.goto("http://localhost:8001/dashboard")

    # Check if Copy button exists (initially hidden)
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_hidden()

    # Select a GEM
    page.wait_for_selector("#gem-nav button")
    page.locator("#gem-nav button").first.click()

    expect(copy_btn).to_be_visible()
    expect(copy_btn).to_have_attribute("aria-label", "Copy prompt to clipboard")

@pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright not installed")
def test_accessibility_attributes(page):
    page.goto("http://localhost:8001/dashboard")

    # Check for ARIA labels on other key elements
    expect(page.locator("#gem-nav")).to_have_attribute("aria-label", "GEM Modules Navigation")
    expect(page.locator("#prompt-content")).to_have_attribute("aria-label", "System Prompt Content")
    expect(page.locator("#chat-history")).to_have_attribute("aria-label", "Refinement History")
    expect(page.locator("#refine-input")).to_have_attribute("aria-label", "Refinement Instructions")
    expect(page.locator("#send-btn")).to_have_attribute("aria-label", "Send Refinement Instruction")

@pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright not installed")
def test_copy_functionality_visual_feedback(page):
    page.goto("http://localhost:8001/dashboard")

    # Mocking clipboard
    page.evaluate("navigator.clipboard.writeText = () => Promise.resolve()")

    page.wait_for_selector("#gem-nav button")
    page.locator("#gem-nav button").first.click()

    copy_btn = page.locator("#copy-btn")
    copy_text = page.locator("#copy-text")

    expect(copy_text).to_have_text("Copiar")

    copy_btn.click()

    # Verify feedback
    expect(copy_text).to_have_text("¡Copiado!")
    expect(copy_btn).to_have_class(re.compile(r".*bg-green-600.*"))

    # Wait for reset
    time.sleep(2.5)
    expect(copy_text).to_have_text("Copiar")
    expect(copy_btn).to_have_class(re.compile(r".*bg-slate-700.*"))
