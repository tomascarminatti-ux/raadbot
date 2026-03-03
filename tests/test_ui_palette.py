import pytest
try:
    from playwright.sync_api import Page, expect
except ImportError:
    pass

@pytest.mark.skipif("playwright" not in globals() and "Page" not in globals(), reason="Playwright not installed")
def test_dashboard_ui_improvements(page: Page, context):
    context.grant_permissions(['clipboard-write', 'clipboard-read'])
    # Go to the dashboard
    page.goto("http://localhost:8000/dashboard")

    # Check for accessibility labels
    # 1. Refine input aria-label
    refine_input = page.get_by_label("Instrucciones para refinar el GEM")
    expect(refine_input).to_be_visible()

    # 2. Wait for GEMS to load and check for aria-labels in sidebar
    # GEMS are loaded via fetch to /api/v1/gems
    # We wait for the first button to appear
    page.wait_for_selector("#gem-nav button")

    gem_buttons = page.locator("#gem-nav button")
    count = gem_buttons.count()
    assert count > 0

    import re
    for i in range(count):
        expect(gem_buttons.nth(i)).to_have_attribute("aria-label", re.compile(r"Seleccionar GEM\d"))

    # 3. Check that the copy button is hidden initially
    copy_btn = page.locator("#copy-btn")
    expect(copy_btn).to_be_hidden()

    # 4. Select a GEM
    gem_buttons.first.click()

    # 5. Check that the copy button is now visible
    expect(copy_btn).to_be_visible()
    expect(copy_btn).to_have_attribute("aria-label", "Copiar prompt al portapapeles")

    # 6. Test copy to clipboard (optional, might be hard in headless)
    # We can at least check if clicking it triggers the visual feedback
    copy_btn.click()
    expect(copy_btn).to_have_text("✅ Copiado")

    # Wait for it to revert
    page.wait_for_timeout(2500)
    expect(copy_btn).to_have_text("📋 Copiar")
