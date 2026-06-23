import pytest
import re
from playwright.sync_api import Page, expect
import time
import subprocess
import os

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

def test_dashboard_copy_button_exists(page):
    page.goto("http://localhost:8001/dashboard")

    # Check if Copy button exists and has ARIA label
    copy_btn = page.locator("#copy-btn")
    # Initially hidden until GEM is selected
    expect(copy_btn).to_be_hidden()

    # Select a GEM
    page.wait_for_selector("#gem-nav button")
    page.locator("#gem-nav button").first.click()

    expect(copy_btn).to_be_visible()
    expect(copy_btn).to_have_attribute("aria-label", "Copiar prompt al portapapeles")

def test_accessibility_attributes(page):
    page.goto("http://localhost:8001/dashboard")

    # Check for ARIA labels on other key elements
    expect(page.locator("#gem-nav")).to_have_attribute("aria-label", "Navegación de módulos GEM")
    expect(page.locator("#prompt-content")).to_have_attribute("aria-label", "Contenido del prompt del sistema")
    expect(page.locator("#chat-history")).to_have_attribute("aria-label", "Historial de refinamiento")
    expect(page.locator("#refine-input")).to_have_attribute("aria-label", "Instrucciones para refinar el prompt")
    expect(page.locator("#send-btn")).to_have_attribute("aria-label", "Enviar instrucción de refinamiento")

def test_copy_functionality_visual_feedback(page):
    page.goto("http://localhost:8001/dashboard")

    # Mocking clipboard as it's often restricted in headless browsers
    page.evaluate("navigator.clipboard.writeText = () => Promise.resolve()")

    # Select a GEM first to enable functionality (simulated)
    # We need to wait for GEMS to load
    page.wait_for_selector("#gem-nav button")
    page.locator("#gem-nav button").first.click()

    copy_btn = page.locator("#copy-btn")
    copy_text = page.locator("#copy-text")

    expect(copy_text).to_have_text("Copiar")

    copy_btn.click()

    # Verify feedback
    expect(copy_text).to_have_text("¡Copiado!")
    expect(copy_btn).to_have_class(re.compile(r".*bg-green-600.*"))

    # Wait for reset (2 seconds in code, so wait slightly more)
    time.sleep(2.5)
    expect(copy_text).to_have_text("Copiar")
    expect(copy_btn).to_have_class(re.compile(r".*bg-slate-700.*"))
