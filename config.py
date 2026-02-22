import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Gating Thresholds
SCORING_CUTOFF = float(os.getenv("SCORING_CUTOFF", "0.4"))
QA_GATE_CUTOFF = float(os.getenv("QA_GATE_CUTOFF", "0.85"))

THRESHOLDS = {
    "gem1": 6,
    "gem2": 6,
    "gem3": 6,
    "gem4": 7,
}

# Max retries for validation/JSON failures
MAX_RETRIES_ON_BLOCK = int(os.getenv("MAX_RETRIES_ON_BLOCK", "2"))

# Gemini Pricing (per 1M tokens) - Update as needed
# Prices for Gemini 2.0 Flash (current as of late 2024/early 2025)
PRICE_PROMPT_1M = 0.10  # Example price, adjust to reality
PRICE_COMPLETION_1M = 0.40 # Example price, adjust to reality

# GEM Technical Configurations (System Prompts v2.0)
GEM_CONFIGS = {
    "gem1": {"temperature": 0.2, "top_p": 0.7, "max_tokens": 2500},
    "gem2": {"temperature": 0.4, "top_p": 0.85, "max_tokens": 3000},
    "gem3": {"temperature": 0.3, "top_p": 0.75, "max_tokens": 3500},
    "gem4": {"temperature": 0.1, "top_p": 0.5, "max_tokens": 4000},
    "gem5": {"temperature": 0.3, "top_p": 0.8, "max_tokens": 2000},
}

# Google Drive Settings
DRIVE_CREDENTIALS_PATH = os.getenv("DRIVE_CREDENTIALS_PATH", "credentials.json")
DRIVE_TOKEN_FILE = "token.json"
