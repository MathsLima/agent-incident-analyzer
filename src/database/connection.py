"""
Database connection management for SQLite.
"""

from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import get_config


class DatabaseConnection:
    """Manages SQLite database connection."""

    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            database_url: Database URL. If not provided, uses config.
        """
        if database_url is None:
            config = get_config()
            database_url = config.database_url

        # Ensure data directory exists
        db_path = database_url.replace("sqlite:///", "")
        db_file = Path(db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)

        self.engine: Engine = create_engine(
            database_url,
            echo=False,
            connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_session(self) -> Session:
        """
        Get a new database session.

        Returns:
            SQLAlchemy Session instance.
        """
        return self.SessionLocal()

    def create_tables(self) -> None:
        """Create all tables in the database."""
        from src.database.schema import Base
        Base.metadata.create_all(bind=self.engine)


# Global database connection instance
_db_connection: Optional[DatabaseConnection] = None


def get_db() -> DatabaseConnection:
    """
    Get the global database connection instance.

    Returns:
        DatabaseConnection instance.
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection
