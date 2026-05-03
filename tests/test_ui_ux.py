import pytest
from playwright.sync_api import Page, expect

def test_dashboard_elements(page: Page):
    # Navigate to the dashboard
    # Note: This assumes the server is running on localhost:8000
    page.goto("http://127.0.0.1:8000/dashboard")

    # Check for the title
    expect(page).to_have_title("Raadbot Control Panel")

    # Verify the "Copiar" button exists
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_visible()
    expect(copy_btn).to_contain_text("Copiar")

    # Verify accessibility attributes
    refine_input = page.locator("#refine-input")
    expect(refine_input).to_have_attribute("aria-labelledby", "refine-label")

    refine_label = page.locator("#refine-label")
    expect(refine_label).to_be_visible()
    expect(refine_label).to_have_text("Refinamiento IA")

    send_btn = page.locator("#send-btn")
    expect(send_btn).to_have_attribute("aria-label", "Refinar Prompt")

    logs_container = page.locator("#logs-container")
    expect(logs_container).to_have_attribute("role", "log")
    expect(logs_container).to_have_attribute("aria-live", "polite")

def test_copy_button_feedback(page: Page):
    page.goto("http://127.0.0.1:8000/dashboard")

    # Grant clipboard permissions
    context = page.context
    context.grant_permissions(['clipboard-read', 'clipboard-write'])

    copy_btn = page.locator("#copy-btn")
    copy_btn.click()

    # Check for feedback text
    expect(page.locator("#copy-text")).to_have_text("Copiado!")
    expect(page.locator("#copy-icon")).to_have_text("✅")

    # Check that it reverts (wait a bit more than 2s)
    page.wait_for_timeout(2500)
    expect(page.locator("#copy-text")).to_have_text("Copiar")
    expect(page.locator("#copy-icon")).to_have_text("📋")
