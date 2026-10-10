#!/usr/bin/env python3
"""
Test the orchestrator workflow without requiring LLM API key.

Uses require_api_key=False to allow testing with mocked responses.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.orchestrator import IncidentOrchestrator


def test_orchestrator():
    """Test the orchestrator with a simple request."""
    print("=" * 60)
    print("Agent Incident Analyzer - Orchestrator Test")
    print("=" * 60)

    # Note: This requires NVIDIA_API_KEY to be configured
    # If not configured, it will fail with a clear error message
    print("\nNote: This test requires NVIDIA_API_KEY to be configured.")
    print("If not configured, you will see an error message - this is expected.\n")

    try:
        # Create orchestrator (requires API key)
        orchestrator = IncidentOrchestrator(require_api_key=True)

        # Test with a simple request
        request = "The payments API is returning HTTP 500 errors."
        print(f"Testing request: {request}\n")

        result = orchestrator.invoke(request)

        print("=" * 60)
        print("Execution Trace:")
        print("=" * 60)
        for trace in result.execution_trace:
            print(trace)

        print("\n" + "=" * 60)
        print("Final Response:")
        print("=" * 60)
        print(result.final_response)

        print("\n" + "=" * 60)
        print("✓ Orchestrator test completed")
        print("=" * 60)

    except ValueError as e:
        print(f"\n✗ Configuration error: {e}")
        print("\nTo fix this:")
        print("1. Copy .env.example to .env")
        print("2. Add your NVIDIA_API_KEY to .env")
        print("3. Run this test again")
        sys.exit(1)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    test_orchestrator()
