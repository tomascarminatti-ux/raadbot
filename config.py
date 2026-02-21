import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Gating Thresholds
THRESHOLDS = {
    "gem1": 6,
    "gem2": 6,
    "gem3": 6,
    "gem4": 7,
}

# Max retries for validation/JSON failures
MAX_RETRIES_ON_BLOCK = 2

# Gemini Pricing (per 1M tokens) - Update as needed
# Prices for Gemini 2.0 Flash (current as of late 2024/early 2025)
PRICE_PROMPT_1M = 0.10  # Example price, adjust to reality
PRICE_COMPLETION_1M = 0.40 # Example price, adjust to reality

# Google Drive Settings
DRIVE_CREDENTIALS_PATH = os.getenv("DRIVE_CREDENTIALS_PATH", "credentials.json")
DRIVE_TOKEN_FILE = "token.json"
