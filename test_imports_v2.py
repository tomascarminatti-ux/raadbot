import sys
import os

# Add current directory to path to test local imports
sys.path.append(os.getcwd())

try:
    import dotenv
    print("SUCCESS: dotenv imported")
except ImportError as e:
    print(f"FAILURE: dotenv import failed: {e}")

try:
    import httpx
    print("SUCCESS: httpx imported")
except ImportError as e:
    print(f"FAILURE: httpx import failed: {e}")

try:
    import config
    print("SUCCESS: local 'config' imported")
except ImportError as e:
    print(f"FAILURE: local 'config' import failed: {e}")

try:
    from utils.gem_core import GEMClient
    print("SUCCESS: 'utils.gem_core' imported")
except ImportError as e:
    print(f"FAILURE: 'utils.gem_core' import failed: {e}")
