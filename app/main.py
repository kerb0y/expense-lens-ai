"""ExpenseLens AI, FastAPI application.

Run locally:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/ for the web app and
http://127.0.0.1:8000/docs for the interactive API docs.

Data is stored in a local SQLite file (expenses.db) so a small UMKM
can run this without a database server. Set EXPENSE_DB_PATH to use a
different file, for example in tests.
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .categorizer import categorize
from .schemas import CategorizeRequest, TransactionCreate
from .store import add_transaction, connect, delete_transaction, list_transactions
from .summary import summarize

app = FastAPI(
    title="ExpenseLens AI",
    description=(
        "Pencatatan keuangan UMKM dengan kategorisasi otomatis. "
        "Tulis catatan transaksi dalam bahasa sehari-hari, sistem "
        "menebak kategorinya, dan ringkasan laba serta per kategori "
        "dihitung otomatis."
    ),
    version="1.0.0",
)

FRONTEND = Path(__file__).resolve().parents[1] / "frontend" / "index.html"


@app.get("/")
def root():
    return FileResponse(FRONTEND)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/categorize")
def categorize_endpoint(payload: CategorizeRequest) -> dict:
    return categorize(payload.note, payload.type)


@app.post("/api/transactions", status_code=201)
def create_transaction(payload: TransactionCreate) -> dict:
    category = payload.category
    if not category:
        category = categorize(payload.note, payload.type)["category"]
    conn = connect()
    try:
        return add_transaction(
            conn,
            {
                "type": payload.type,
                "amount": payload.amount,
                "category": category,
                "note": payload.note,
                "date": payload.date,
            },
        )
    finally:
        conn.close()


@app.get("/api/transactions")
def get_transactions(type: str | None = None, category: str | None = None) -> dict:
    conn = connect()
    try:
        items = list_transactions(conn, txn_type=type, category=category)
    finally:
        conn.close()
    return {"transactions": items, "count": len(items)}


@app.get("/api/summary")
def get_summary() -> dict:
    conn = connect()
    try:
        items = list_transactions(conn)
    finally:
        conn.close()
    return summarize(items)


@app.delete("/api/transactions/{txn_id}")
def remove_transaction(txn_id: int) -> dict:
    conn = connect()
    try:
        deleted = delete_transaction(conn, txn_id)
    finally:
        conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    return {"deleted": True, "id": txn_id}
