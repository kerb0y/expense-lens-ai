"""SQLite storage for transactions, using only the standard library."""
import os
import sqlite3
from pathlib import Path


def db_path() -> Path:
    override = os.environ.get("EXPENSE_DB_PATH")
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[1] / "expenses.db"


def connect(path: Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path or db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT NOT NULL,
            date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def add_transaction(conn: sqlite3.Connection, txn: dict) -> dict:
    cur = conn.execute(
        "INSERT INTO transactions (type, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
        (txn["type"], txn["amount"], txn["category"], txn["note"], txn["date"]),
    )
    conn.commit()
    return get_transaction(conn, cur.lastrowid)


def get_transaction(conn: sqlite3.Connection, txn_id: int) -> dict | None:
    row = conn.execute(
        "SELECT * FROM transactions WHERE id = ?", (txn_id,)
    ).fetchone()
    return dict(row) if row else None


def list_transactions(
    conn: sqlite3.Connection, txn_type: str | None = None, category: str | None = None
) -> list[dict]:
    query = "SELECT * FROM transactions"
    conditions: list[str] = []
    params: list = []
    if txn_type:
        conditions.append("type = ?")
        params.append(txn_type)
    if category:
        conditions.append("category = ?")
        params.append(category)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY date DESC, id DESC"
    return [dict(r) for r in conn.execute(query, params).fetchall()]


def delete_transaction(conn: sqlite3.Connection, txn_id: int) -> bool:
    cur = conn.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
    conn.commit()
    return cur.rowcount > 0
