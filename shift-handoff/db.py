"""
Database layer for Shift Handoff Notes.

Uses SQLite so the whole app runs with zero external setup — no database
server to install or configure. That's a deliberate choice: the target
user is a shift worker or team lead, not someone who wants to provision
infrastructure before trying a tool.
"""

import sqlite3
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "handoffs.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS handoffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                shift_date TEXT NOT NULL,
                shift_period TEXT NOT NULL,
                department TEXT NOT NULL,
                outgoing_employee TEXT NOT NULL,
                tasks_completed TEXT,
                tasks_pending TEXT,
                issues TEXT,
                is_urgent INTEGER NOT NULL DEFAULT 0,
                notes TEXT,
                acknowledged INTEGER NOT NULL DEFAULT 0,
                acknowledged_by TEXT,
                acknowledged_at TEXT
            )
        """)


def add_handoff(shift_date, shift_period, department, outgoing_employee,
                tasks_completed, tasks_pending, issues, is_urgent, notes):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO handoffs (
                created_at, shift_date, shift_period, department,
                outgoing_employee, tasks_completed, tasks_pending,
                issues, is_urgent, notes, acknowledged
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            datetime.now().isoformat(timespec="seconds"),
            shift_date, shift_period, department, outgoing_employee,
            tasks_completed, tasks_pending, issues, int(is_urgent), notes
        ))


def get_handoffs(department=None, only_unacknowledged=False):
    query = "SELECT * FROM handoffs WHERE 1=1"
    params = []
    if department and department != "All":
        query += " AND department = ?"
        params.append(department)
    if only_unacknowledged:
        query += " AND acknowledged = 0"
    query += " ORDER BY created_at DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def get_departments():
    with get_connection() as conn:
        rows = conn.execute("SELECT DISTINCT department FROM handoffs ORDER BY department").fetchall()
        return [row["department"] for row in rows]


def acknowledge_handoff(handoff_id, acknowledged_by):
    with get_connection() as conn:
        conn.execute("""
            UPDATE handoffs
            SET acknowledged = 1, acknowledged_by = ?, acknowledged_at = ?
            WHERE id = ?
        """, (acknowledged_by, datetime.now().isoformat(timespec="seconds"), handoff_id))


def get_summary_counts():
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM handoffs").fetchone()[0]
        unacknowledged = conn.execute("SELECT COUNT(*) FROM handoffs WHERE acknowledged = 0").fetchone()[0]
        urgent_open = conn.execute(
            "SELECT COUNT(*) FROM handoffs WHERE is_urgent = 1 AND acknowledged = 0"
        ).fetchone()[0]
        return {"total": total, "unacknowledged": unacknowledged, "urgent_open": urgent_open}


def seed_example_data():
    """Pre-loads a couple of example handoffs so a first-time visitor sees
    the app's value immediately, without needing a second person to hand
    off to."""
    with get_connection() as conn:
        existing = conn.execute("SELECT COUNT(*) FROM handoffs").fetchone()[0]
        if existing > 0:
            return  # don't reseed if data already exists

    add_handoff(
        shift_date=datetime.now().strftime("%Y-%m-%d"),
        shift_period="Night",
        department="Nursing - Floor 3",
        outgoing_employee="J. Alvarez",
        tasks_completed="Vitals checked for all patients at 2am and 5am rounds. Room 312 IV bag replaced.",
        tasks_pending="Room 308 patient waiting on updated pain medication order from Dr. Kim.",
        issues="Room 315 patient reported dizziness at 4:45am, vitals normal, but flagged for morning follow-up.",
        is_urgent=True,
        notes="Family in Room 312 asked to be updated as soon as the attending rounds in the morning.",
    )
    add_handoff(
        shift_date=datetime.now().strftime("%Y-%m-%d"),
        shift_period="Evening",
        department="Warehouse - Receiving",
        outgoing_employee="M. Chen",
        tasks_completed="Unloaded and logged 3 incoming shipments (PO#4471, 4472, 4478).",
        tasks_pending="PO#4478 short by 2 pallets, waiting on carrier confirmation.",
        issues="",
        is_urgent=False,
        notes="Forklift #2 making a grinding noise, still usable but should get looked at.",
    )
