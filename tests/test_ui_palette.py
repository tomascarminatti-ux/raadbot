import asyncio
import pytest
from playwright.async_api import async_playwright, expect
import uvicorn
import multiprocessing
import time
import os

# Define a simple helper to start the server
def run_server():
    from api import app
    # Use a different port to avoid conflicts
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

@pytest.mark.asyncio
async def test_copy_button_visibility_and_feedback():
    # Start the server in a separate process
    proc = multiprocessing.Process(target=run_server, daemon=True)
    proc.start()

    # Give the server some time to start
    time.sleep(5)

    async with async_playwright() as p:
        # Launch browser with clipboard permissions
        browser = await p.chromium.launch(headless=True)
        # Grant clipboard permissions for localhost
        context = await browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
        page = await context.new_page()

        try:
            # Navigate to the dashboard
            await page.goto("http://127.0.0.1:8001/dashboard", wait_until="networkidle")

            # 1. Verify Copy button is hidden initially
            copy_btn = page.locator("#copy-btn")
            assert await copy_btn.is_hidden()

            # 2. Wait for GEMs to load
            await page.wait_for_selector("#gem-nav button")
            gem1_btn = page.locator("#gem-nav button").first
            await gem1_btn.click()

            # 3. Verify Copy button is now visible
            await page.wait_for_selector("#copy-btn", state="visible")
            assert await copy_btn.is_visible()

            # 4. Verify ARIA labels
            aria_label = await copy_btn.get_attribute("aria-label")
            assert aria_label == "Copiar prompt al portapapeles"

            # 5. Click Copy button and verify feedback
            await copy_btn.click()

            # Wait for text update
            btn_text = page.locator("#copy-text")
            await page.wait_for_function('document.getElementById("copy-text").innerText === "✅ ¡Copiado!"')

            final_text = await btn_text.inner_text()
            assert final_text == "✅ ¡Copiado!"

            # Verify updated aria-label
            new_aria_label = await copy_btn.get_attribute("aria-label")
            assert new_aria_label == "¡Prompt copiado con éxito!"

            # 6. Verify accessibility: aria-hidden elements
            sidebar_header = page.locator("aside h1")
            robot_span = sidebar_header.locator("span").first
            assert await robot_span.get_attribute("aria-hidden") == "true"

            # 7. Check the rocket in the send button
            send_btn_span = page.locator("#send-btn span").first
            assert await send_btn_span.get_attribute("aria-hidden") == "true"

            # 8. Check aria-live on chat-history
            chat_history = page.locator("#chat-history")
            assert await chat_history.get_attribute("aria-live") == "polite"

            # 9. Verify localized "Solo lectura" badge
            read_only_badge = page.locator('span:has-text("Solo lectura")')
            assert await read_only_badge.is_visible()

        finally:
            await context.close()
            await browser.close()
            proc.terminate()
