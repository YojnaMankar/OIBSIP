"""
Database Module - OASIS INFOBYTE Task 2: BMI Calculator (Advanced)
Handles SQLite database persistence, schema creation, and queries.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bmi_records.db")


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Establish and return a connection to the SQLite database with row factory."""
    path = db_path or DEFAULT_DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """
    Initialize SQLite database and create required tables if they don't exist.
    Creates an index on user_name to optimize multi-user query performance.
    """
    path = db_path or DEFAULT_DB_PATH
    conn = get_connection(path)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    date_time TEXT NOT NULL
                );
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_bmi_user ON bmi_records (user_name);
                """
            )
    finally:
        conn.close()


def insert_record(
    user_name: str,
    weight: float,
    height: float,
    bmi: float,
    category: str,
    date_time: Optional[str] = None,
    db_path: Optional[str] = None
) -> int:
    """
    Insert a new BMI measurement record.
    If date_time is not provided, current system timestamp is used.
    Returns the newly inserted record ID.
    """
    timestamp = date_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO bmi_records (user_name, weight, height, bmi, category, date_time)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (user_name.strip(), float(weight), float(height), float(bmi), category, timestamp)
            )
            return cursor.lastrowid
    finally:
        conn.close()


def get_records(user_name: Optional[str] = None, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetch BMI records.
    If user_name is specified (and not 'All Users'), filters records for that specific user.
    Records are ordered chronologically (oldest to newest for graphing, or formatted for table).
    """
    conn = get_connection(db_path)
    try:
        if user_name and user_name != "All Users":
            cursor = conn.execute(
                """
                SELECT id, user_name, weight, height, bmi, category, date_time
                FROM bmi_records
                WHERE user_name = ?
                ORDER BY id ASC;
                """,
                (user_name.strip(),)
            )
        else:
            cursor = conn.execute(
                """
                SELECT id, user_name, weight, height, bmi, category, date_time
                FROM bmi_records
                ORDER BY id DESC;
                """
            )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_all_users(db_path: Optional[str] = None) -> List[str]:
    """
    Retrieve a sorted list of unique usernames that exist in the database.
    """
    conn = get_connection(db_path)
    try:
        cursor = conn.execute(
            """
            SELECT DISTINCT user_name
            FROM bmi_records
            ORDER BY user_name COLLATE NOCASE ASC;
            """
        )
        return [row["user_name"] for row in cursor.fetchall()]
    finally:
        conn.close()


def delete_record(record_id: int, db_path: Optional[str] = None) -> bool:
    """
    Delete a specific record by its primary key ID.
    Returns True if a record was deleted, False otherwise.
    """
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.execute(
                "DELETE FROM bmi_records WHERE id = ?;",
                (record_id,)
            )
            return cursor.rowcount > 0
    finally:
        conn.close()


def clear_user_history(user_name: str, db_path: Optional[str] = None) -> int:
    """
    Delete all records for a given user.
    Returns the count of deleted records.
    """
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.execute(
                "DELETE FROM bmi_records WHERE user_name = ?;",
                (user_name.strip(),)
            )
            return cursor.rowcount
    finally:
        conn.close()
