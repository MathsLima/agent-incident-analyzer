#!/usr/bin/env python3
"""
Initialize and seed the database with demonstration data.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database import get_db

if __name__ == "__main__":
    print("Initializing database...")
    db = get_db()
    db.create_tables()
    print("✓ Database tables created")

    print("Seeding database with demonstration data...")
    from src.database.seed import seed_database
    seed_database()
    print("✓ Database seeded successfully")
