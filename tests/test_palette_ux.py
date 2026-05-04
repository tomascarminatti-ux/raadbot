import pytest
import re
from playwright.sync_api import Page, expect

def test_copy_button_exists_and_functional(browser):
    context = browser.new_context()
    context.grant_permissions(['clipboard-read', 'clipboard-write'])
    page = context.new_page()

    # Go to the dashboard
    page.goto("http://127.0.0.1:8000/dashboard")

    # Check if the copy button exists
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_visible()

    # Check ARIA label
    expect(copy_btn).to_have_attribute("aria-label", "Copiar prompt al portapapeles")

    # Check initial text
    expect(page.locator("#copy-text")).to_have_text("Copiar")

    # Click the button
    copy_btn.click()

    # Check if text changes to "Copiado!"
    expect(page.locator("#copy-text")).to_have_text("Copiado!", timeout=10000)
    expect(page.locator("#copy-icon")).to_have_text("✅")

    # Verify it has success colors (Tailwind classes)
    expect(copy_btn).to_have_class(re.compile(r"bg-green-500"))

    context.close()
