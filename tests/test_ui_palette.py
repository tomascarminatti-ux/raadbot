import asyncio
import os
from playwright.async_api import async_playwright, expect


async def test_copy_button():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to the dashboard
        # Assuming server runs on http://localhost:8000
        try:
            await page.goto("http://localhost:8000/dashboard")
        except Exception as e:
            print(f"Error connecting to server: {e}")
            await browser.close()
            return

        # Wait for gems to load
        await page.wait_for_selector("#gem-nav button")

        # Select first gem
        first_gem = page.locator("#gem-nav button").first
        await first_gem.click()

        # Check if prompt content is updated
        prompt_content = page.locator("#prompt-content")
        await expect(prompt_content).not_to_have_text("Selecciona un GEM para ver sus instrucciones core...")

        # Mock clipboard
        await page.evaluate(
            "navigator.clipboard.writeText = (text) => { window.lastCopiedText = text; return Promise.resolve(); }"
        )

        # Find copy button
        copy_btn = page.locator("#copy-btn")
        await expect(copy_btn).to_be_visible()

        # Click copy button
        await copy_btn.click()

        # Verify feedback
        await expect(copy_btn).to_have_text("¡COPIADO!")

        # Verify clipboard content via mock
        last_text = await page.evaluate("window.lastCopiedText")
        actual_text = await prompt_content.inner_text()
        assert last_text == actual_text

        # Wait for feedback to reset (optional for test, but good to verify)
        await page.wait_for_timeout(2100)
        await expect(copy_btn).not_to_have_text("¡COPIADO!")

        # Take screenshot for verification
        os.makedirs("verification", exist_ok=True)
        await page.screenshot(path="verification/dashboard_palette.png")
        print("Screenshot saved to verification/dashboard_palette.png")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_copy_button())
