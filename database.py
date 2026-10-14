"""Database operations for the Campus Lost & Found Tracker."""

import sqlite3
from pathlib import Path

# The database is created beside this Python file when the app is first run.
DATABASE_FILE = Path(__file__).resolve().parent / "lost_found.db"


def connect_database(database_file=DATABASE_FILE):
    """Open a connection to the SQLite database."""
    connection = sqlite3.connect(database_file)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_file=DATABASE_FILE):
    """Create the reports table if it does not already exist."""
    with connect_database(database_file) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL CHECK (report_type IN ('Lost', 'Found')),
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                report_date TEXT NOT NULL,
                description TEXT NOT NULL,
                contact_info TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'Open'
                    CHECK (status IN ('Open', 'Resolved')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def add_report(report, database_file=DATABASE_FILE):
    """Save a new lost or found report and return its database ID."""
    with connect_database(database_file) as connection:
        cursor = connection.execute(
            """
            INSERT INTO reports
                (report_type, item_name, category, location, report_date,
                 description, contact_info)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report["report_type"],
                report["item_name"],
                report["category"],
                report["location"],
                report["report_date"],
                report["description"],
                report.get("contact_info", ""),
            ),
        )
        return cursor.lastrowid


def get_reports(search_text="", database_file=DATABASE_FILE):
    """Return reports, optionally searching common fields."""
    search_value = f"%{search_text.strip()}%"
    with connect_database(database_file) as connection:
        rows = connection.execute(
            """
            SELECT id, report_type, item_name, category, location,
                   report_date, description, contact_info, status
            FROM reports
            WHERE item_name LIKE ?
               OR category LIKE ?
               OR location LIKE ?
               OR description LIKE ?
               OR report_type LIKE ?
               OR status LIKE ?
            ORDER BY CASE status WHEN 'Open' THEN 0 ELSE 1 END,
                     report_date DESC, id DESC
            """,
            (search_value,) * 6,
        ).fetchall()
        return [dict(row) for row in rows]


def get_report(report_id, database_file=DATABASE_FILE):
    """Return one report by ID, or None if it no longer exists."""
    with connect_database(database_file) as connection:
        row = connection.execute(
            "SELECT * FROM reports WHERE id = ?", (report_id,)
        ).fetchone()
        return dict(row) if row else None


def mark_resolved(report_id, database_file=DATABASE_FILE):
    """Mark a report as resolved."""
    with connect_database(database_file) as connection:
        cursor = connection.execute(
            "UPDATE reports SET status = 'Resolved' WHERE id = ?",
            (report_id,),
        )
        return cursor.rowcount > 0


def delete_report(report_id, database_file=DATABASE_FILE):
    """Delete a report by ID."""
    with connect_database(database_file) as connection:
        cursor = connection.execute(
            "DELETE FROM reports WHERE id = ?", (report_id,)
        )
        return cursor.rowcount > 0
