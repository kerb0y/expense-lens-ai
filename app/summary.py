"""Summary aggregation over a list of transaction dicts."""
from collections import defaultdict


def summarize(transactions: list[dict]) -> dict:
    total_in = sum(t["amount"] for t in transactions if t["type"] == "pemasukan")
    total_out = sum(t["amount"] for t in transactions if t["type"] == "pengeluaran")
    per_category: dict[str, float] = defaultdict(float)
    per_month: dict[str, dict[str, float]] = defaultdict(
        lambda: {"pemasukan": 0.0, "pengeluaran": 0.0}
    )
    for t in transactions:
        sign = t["amount"] if t["type"] == "pemasukan" else -t["amount"]
        per_category[t["category"]] += t["amount"]
        month = str(t["date"])[:7]
        per_month[month][t["type"]] += t["amount"]
        _ = sign
    return {
        "total_pemasukan": round(total_in, 2),
        "total_pengeluaran": round(total_out, 2),
        "laba": round(total_in - total_out, 2),
        "jumlah_transaksi": len(transactions),
        "per_kategori": dict(sorted(per_category.items())),
        "per_bulan": dict(sorted(per_month.items())),
    }
