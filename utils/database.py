"""SQLite database helper for SQL practice exercises."""
import sqlite3
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


class SQLiteHelper:
    """Helper class for managing SQLite databases for SQL exercises."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database. If None, uses in-memory database.
        """
        self.db_path = db_path or ":memory:"
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def connect(self):
        """Connect to database."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        # Enable foreign keys
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def execute_script(self, script: str) -> None:
        """Execute SQL script (multiple statements).

        Args:
            script: SQL script to execute
        """
        self.cursor.executescript(script)
        self.conn.commit()

    def execute_file(self, file_path: str) -> None:
        """Execute SQL file.

        Args:
            file_path: Path to SQL file
        """
        with open(file_path, 'r') as f:
            script = f.read()
        self.execute_script(script)

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results as list of dicts.

        Args:
            query: SELECT query to execute

        Returns:
            List of dictionaries with column names as keys
        """
        self.cursor.execute(query)
        columns = [desc[0] for desc in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def load_schema(self, schema_file: str) -> None:
        """Load database schema from file.

        Args:
            schema_file: Path to schema SQL file
        """
        self.execute_file(schema_file)

    def load_data(self, data_file: str) -> None:
        """Load sample data from file.

        Args:
            data_file: Path to data SQL file
        """
        self.execute_file(data_file)

    def get_table_names(self) -> List[str]:
        """Get list of all tables in database.

        Returns:
            List of table names
        """
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a table.

        Args:
            table_name: Name of table

        Returns:
            List of column information dictionaries
        """
        query = f"PRAGMA table_info({table_name})"
        self.cursor.execute(query)
        columns = [desc[0] for desc in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def compare_results(self, result1: List[Dict[str, Any]],
                       result2: List[Dict[str, Any]],
                       order_matters: bool = False) -> bool:
        """Compare two query results.

        Args:
            result1: First result set
            result2: Second result set
            order_matters: Whether row order should be considered

        Returns:
            True if results are equal, False otherwise
        """
        if len(result1) != len(result2):
            return False

        if order_matters:
            return result1 == result2
        else:
            # Sort both lists by converting dicts to sorted tuples
            sorted1 = sorted([tuple(sorted(d.items())) for d in result1])
            sorted2 = sorted([tuple(sorted(d.items())) for d in result2])
            return sorted1 == sorted2


def setup_exercise_database(exercise_path: str) -> SQLiteHelper:
    """Set up database for a SQL exercise.

    Args:
        exercise_path: Path to exercise directory

    Returns:
        Configured SQLiteHelper instance
    """
    db = SQLiteHelper()
    db.connect()

    schema_file = os.path.join(exercise_path, "schema.sql")
    data_file = os.path.join(exercise_path, "sample_data.sql")

    if os.path.exists(schema_file):
        db.load_schema(schema_file)

    if os.path.exists(data_file):
        db.load_data(data_file)

    return db
