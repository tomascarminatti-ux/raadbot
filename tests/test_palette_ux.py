import pytest
from bs4 import BeautifulSoup
import os

def test_copy_button_exists():
    path = "templates/dashboard.html"
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Check if copy button exists
    copy_btn = soup.find("button", id="copy-btn")
    assert copy_btn is not None
    assert "onclick=\"copyToClipboard()\"" in str(copy_btn)
    assert copy_btn.get("aria-label") == "Copiar prompt al portapapeles"
    assert "hidden" in copy_btn.get("class") # Should be hidden by default

def test_javascript_functions_present():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    assert "function copyToClipboard()" in html
    assert "document.getElementById('copy-btn').classList.remove('hidden')" in html
