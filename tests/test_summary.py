import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.summary import summarize

TXNS = [
    {"type": "pemasukan", "amount": 250000, "category": "penjualan", "note": "a", "date": "2026-10-27"},
    {"type": "pemasukan", "amount": 120000, "category": "jasa", "note": "b", "date": "2026-10-26"},
    {"type": "pengeluaran", "amount": 50000, "category": "bahan_baku", "note": "c", "date": "2026-10-27"},
    {"type": "pengeluaran", "amount": 150000, "category": "operasional", "note": "d", "date": "2026-10-27"},
]


def test_totals_and_profit():
    s = summarize(TXNS)
    assert s["total_pemasukan"] == 370000
    assert s["total_pengeluaran"] == 200000
    assert s["laba"] == 170000
    assert s["jumlah_transaksi"] == 4


def test_per_category_and_month():
    s = summarize(TXNS)
    assert s["per_kategori"]["penjualan"] == 250000
    assert s["per_bulan"]["2026-10"]["pemasukan"] == 370000


def test_empty_summary():
    s = summarize([])
    assert s["laba"] == 0
    assert s["jumlah_transaksi"] == 0
