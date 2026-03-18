import asyncio
import pytest
from playwright.async_api import async_playwright
import subprocess
import time
import os

@pytest.mark.asyncio
async def test_dashboard_ux_enhancements():
    # Start the server in the background
    server_process = subprocess.Popen(
        ["python3", "-m", "uvicorn", "api:app", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    time.sleep(5)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Grant clipboard permissions
            context = await browser.new_context()
            await context.grant_permissions(["clipboard-read", "clipboard-write"])
            page = await context.new_page()

            await page.goto("http://localhost:8001/dashboard", wait_until="networkidle")

            # 1. Verify "Solo lectura" badge
            badge = page.get_by_text("Solo lectura")
            assert await badge.is_visible(), "Badge 'Solo lectura' should be visible"

            # 2. Verify "Copy" button is hidden initially
            copy_btn = page.locator("#copy-btn")
            assert not await copy_btn.is_visible(), "Copy button should be hidden initially"

            # 3. Select a GEM and verify copy button appears
            # Wait for GEMs to load
            await page.wait_for_selector("#gem-nav button")
            gem_btn = page.locator("#gem-nav button").first
            # Inner text includes the span with arrow, we only want the name
            gem_span = gem_btn.locator("span").first
            gem_name = await gem_span.inner_text()
            await gem_btn.click()

            assert await copy_btn.is_visible(), "Copy button should be visible after selecting a GEM"

            # 4. Verify aria-label on GEM buttons
            aria_label = await gem_btn.get_attribute("aria-label")
            assert aria_label == f"Seleccionar {gem_name.strip()}", f"Aria-label mismatch: {aria_label} vs {gem_name.strip()}"

            # 5. Test Copy to Clipboard functionality
            # We can't easily check actual clipboard in headless linux without X11 but we can check visual feedback
            # In some environments, clipboard API might not be available even with permissions granted
            # causing the script to fail before it can update the UI.
            # We'll use a script injection to trigger the feedback if needed,
            # but first let's try to just click and wait a bit.
            await copy_btn.click()
            await page.wait_for_timeout(500)

            # Check for "¡Copiado!" text
            copy_text = page.locator("#copy-text")
            # If clipboard fails, it might not change text.
            # Let's check console logs if it failed.
            assert await copy_text.inner_text() == "¡Copiado!", "Copy feedback text mismatch. Clipboard might have failed in this environment."

            # Check for green classes
            classes = await copy_btn.get_attribute("class")
            assert "text-green-400" in classes, "Copy feedback color class missing"

            # Check for updated aria-label
            new_aria_label = await copy_btn.get_attribute("aria-label")
            assert new_aria_label == "Prompt copiado con éxito", "Copy feedback aria-label mismatch"

            # Wait for reset
            await asyncio.sleep(2.5)
            assert await copy_text.inner_text() == "Copiar", "Copy text should reset"

            await browser.close()
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    asyncio.run(test_dashboard_ux_enhancements())
