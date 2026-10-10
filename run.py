#!/usr/bin/env python3
"""
Main entry point for Agent Incident Analyzer.

Run this script to start the Gradio interface.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.ui import main

if __name__ == "__main__":
    main()
