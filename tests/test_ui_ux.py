import pytest

def test_dashboard_ui_elements(page):
    from playwright.sync_api import expect
    # Go to the dashboard
    page.goto("http://localhost:8000/dashboard")

    # Check if the "Copy" button exists
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_visible()
    expect(copy_btn).to_have_attribute("aria-label", "Copiar prompt al portapapeles")

    # Check if the logs container has accessibility attributes
    logs_container = page.locator("#logs-container")
    expect(logs_container).to_have_attribute("role", "log")
    expect(logs_container).to_have_attribute("aria-live", "polite")

def test_copy_button_interaction(page, context):
    from playwright.sync_api import expect
    # Grant clipboard permissions
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto("http://localhost:8000/dashboard")

    # Select a GEM to populate the prompt
    # Note: This depends on the API being running and returning gems
    # For the sake of UI test, we can wait for the nav to load
    page.wait_for_selector("#gem-nav button")
    page.click("#gem-nav button:first-child")

    # Click the copy button
    page.click("#copy-btn")

    # Verify visual feedback
    expect(page.locator("#copy-text")).to_have_text("¡Copiado!")
    expect(page.locator("#copy-icon")).to_have_text("✅")

    # Verify it reverts after some time (optional, but good)
    # page.wait_for_timeout(2500)
    # expect(page.locator("#copy-text")).to_have_text("Copiar")
