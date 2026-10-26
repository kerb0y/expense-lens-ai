import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ["EXPENSE_DB_PATH"] = str(Path(tempfile.mkdtemp()) / "test.db")

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_summary_flow():
    r = client.post(
        "/api/transactions",
        json={"type": "pengeluaran", "amount": 50000, "note": "beli beras supplier", "date": "2026-10-27"},
    )
    assert r.status_code == 201
    assert r.json()["category"] == "bahan_baku"

    r2 = client.post(
        "/api/transactions",
        json={"type": "pemasukan", "amount": 250000, "note": "penjualan hari ini", "date": "2026-10-27"},
    )
    assert r2.status_code == 201

    summary = client.get("/api/summary").json()
    assert summary["total_pengeluaran"] == 50000
    assert summary["total_pemasukan"] == 250000
    assert summary["laba"] == 200000


def test_categorize_endpoint():
    r = client.post("/api/categorize", json={"note": "bayar listrik", "type": "pengeluaran"})
    assert r.json()["category"] == "operasional"


def test_invalid_amount_rejected():
    r = client.post(
        "/api/transactions",
        json={"type": "pemasukan", "amount": -100, "note": "test", "date": "2026-10-27"},
    )
    assert r.status_code == 422
