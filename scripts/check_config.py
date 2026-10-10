#!/usr/bin/env python3
"""
Simple script to verify configuration loading without requiring full dependencies.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from config import load_config, validate_llm_config

    print("✓ Configuration module imported successfully")

    # Load configuration
    config = load_config()
    print(f"✓ Configuration loaded")
    print(f"  - App Name: {config.app_name}")
    print(f"  - App Env: {config.app_env}")
    print(f"  - Log Level: {config.log_level}")
    print(f"  - Database URL: {config.database_url}")
    print(f"  - NVIDIA Model: {config.nvidia_model}")
    print(f"  - NVIDIA Base URL: {config.nvidia_base_url}")

    # Check if API key is configured
    if config.nvidia_api_key and config.nvidia_api_key != "your_nvidia_api_key_here":
        print(f"  - NVIDIA API Key: {'*' * 20} (configured)")
    else:
        print(f"  - NVIDIA API Key: not configured (this is expected in demo setup)")

    print("\n✓ All configuration checks passed")

except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Note: This script requires pydantic and python-dotenv to be installed.")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
