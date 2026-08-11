"""
Initialize database tables.

Usage:
    python scripts/init_db.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.engine import init_db


def main():
    """Initialize the database."""
    try:
        print("Initializing database...")
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
