#!/usr/bin/env python3
"""
Simple integration test for the Agent Incident Analyzer.

Tests the basic workflow without requiring full LLM integration.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import get_config
from src.database import get_db
from src.mcp import get_service_status, search_logs


def test_configuration():
    """Test configuration loading."""
    print("Testing configuration...")
    config = get_config()
    print(f"✓ App Name: {config.app_name}")
    print(f"✓ Database URL: {config.database_url}")
    print(f"✓ NVIDIA Model: {config.nvidia_model}")


def test_database():
    """Test database connection and data."""
    print("\nTesting database...")
    db = get_db()
    session = db.get_session()

    from src.database.schema import Service
    services = session.query(Service).all()

    print(f"✓ Found {len(services)} services in database")
    for service in services:
        print(f"  - {service.name}: {service.status}")

    session.close()


def test_mcp_tools():
    """Test MCP tools."""
    print("\nTesting MCP tools...")

    # Test get_service_status
    status = get_service_status("payments-api")
    print(f"✓ Service status: {status.get('status', 'unknown')}")

    # Test search_logs
    logs = search_logs("payments-api", level="ERROR", limit=5)
    print(f"✓ Found {logs.get('count', 0)} error logs")


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Agent Incident Analyzer - Integration Tests")
    print("=" * 60)

    try:
        test_configuration()
        test_database()
        test_mcp_tools()

        print("\n" + "=" * 60)
        print("✓ All integration tests passed")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
