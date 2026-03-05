import pytest
from playwright.sync_api import sync_playwright, expect
import time
import re

@pytest.fixture(scope="module")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        # Grant clipboard permissions
        context.grant_permissions(['clipboard-read', 'clipboard-write'])
        yield context
        browser.close()

def test_dashboard_accessibility_and_copy(browser_context):
    page = browser_context.new_page()
    page.goto("http://127.0.0.1:8000/dashboard", wait_until="networkidle")

    # 1. Check aria-label on refinement input
    refine_input = page.locator("#refine-input")
    expect(refine_input).to_have_attribute("aria-label", "Instrucciones de refinamiento")

    # 2. Check aria-live on chat history
    chat_history = page.locator("#chat-history")
    expect(chat_history).to_have_attribute("aria-live", "polite")

    # 3. Check for GEM buttons and their aria-labels
    # We need to wait for the GEMs to load
    page.wait_for_selector("#gem-nav button")
    gem_buttons = page.locator("#gem-nav button")
    expect(gem_buttons).to_have_count(5) # gem1 to gem5

    for i in range(5):
        btn = gem_buttons.nth(i)
        name = btn.locator("span").first.inner_text()
        expect(btn).to_have_attribute("aria-label", f"Seleccionar {name}")

    # 4. Check "Copy to Clipboard" button visibility and functionality
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_hidden()

    # Select a GEM
    gem_buttons.nth(0).click()

    # Button should be visible now
    expect(copy_btn).to_be_visible()

    # Check copy functionality
    prompt_content = page.locator("#prompt-content").inner_text()
    copy_btn.click()

    # Check visual feedback
    copy_text = page.locator("#copy-text")
    expect(copy_text).to_have_text("¡Copiado!")
    expect(copy_btn).to_have_class(re.compile(r"border-green-500"))
    expect(copy_btn).to_have_class(re.compile(r"text-green-400"))

    # Check clipboard content
    # Note: reading from clipboard in headless playwright can be tricky,
    # but since we granted permissions it should work or at least we verified the UI state change.
    clipboard_content = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_content == prompt_content

    # Wait for visual feedback to revert
    time.sleep(2.5)
    expect(copy_text).to_have_text("Copiar")

    page.close()
