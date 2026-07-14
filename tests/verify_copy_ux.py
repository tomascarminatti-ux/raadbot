import pytest
import re
from playwright.sync_api import Page, expect, BrowserContext

@pytest.fixture(scope="function", autouse=True)
def give_permissions(context: BrowserContext):
    context.grant_permissions(["clipboard-read", "clipboard-write"])

def test_copy_button_interaction(page: Page):
    # Go to dashboard
    page.goto("http://localhost:8000/dashboard")

    # Wait for gems to load
    page.wait_for_selector("#btn-gem1")

    # Select a GEM
    page.click("#btn-gem1")

    # Check if prompt content is visible
    prompt_content = page.locator("#prompt-content")
    expect(prompt_content).not_to_have_text("Selecciona un GEM para ver sus instrucciones core...")

    # Check Copy button initial state
    copy_btn = page.locator("#copy-btn")
    copy_btn_text = page.locator("#copy-btn-text")
    expect(copy_btn_text).to_have_text("Copiar")

    # Click Copy button
    copy_btn.click()

    # Check success state
    expect(copy_btn_text).to_have_text("Copiado")
    expect(copy_btn).to_have_class(re.compile(r"bg-green-600"))

    # Switch GEM and check if state resets
    page.click("#btn-gem2")
    expect(copy_btn_text).to_have_text("Copiar")
    expect(copy_btn).to_have_class(re.compile(r"bg-slate-700"))

def test_localization_and_a11y(page: Page):
    page.goto("http://localhost:8000/dashboard")

    # Check localized badge
    expect(page.get_by_text("Solo lectura")).to_be_visible()

    # Check ARIA labels
    expect(page.get_by_label("Copiar prompt al portapapeles")).to_be_visible()
    expect(page.get_by_label("Contenido del prompt")).to_be_visible()

    # Check focus-visible (simulated by focus)
    copy_btn = page.locator("#copy-btn")
    copy_btn.focus()
    expect(copy_btn).to_have_class(re.compile(r"focus-visible:ring-2"))
