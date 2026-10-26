"""Rule-based transaction categorizer for Indonesian UMKM notes.

The rules are transparent keyword lists, not a black box. A note that
matches a keyword list gets that category with high confidence, a note
with no match falls back to "lainnya" with low confidence so the user
can correct it. Corrections are the future training data for a learned
model, but this version never pretends to be more certain than it is.
"""
import re

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "bahan_baku": [
        "beras", "tepung", "gula", "minyak", "telur", "daging", "ayam",
        "sayur", "buah", "bahan", "supplier", "stok", "kemasan",
        "kardus", "botol", "kopi", "susu", "mentega", "bumbu",
    ],
    "operasional": [
        "listrik", "air", "internet", "wifi", "sewa", "kos", "transport",
        "bensin", "parkir", "pulsa", "kuota", "ongkir", "kurir",
        "kebersihan", "perawatan", "servis alat",
    ],
    "gaji": ["gaji", "upah", "honor", "thr", "bonus karyawan", "pegawai"],
    "pemasaran": [
        "iklan", "promosi", "endorse", "ads", "desain", "banner",
        "brosur", "foto produk", "marketplace fee",
    ],
    "peralatan": [
        "mesin", "alat", "printer", "laptop", "komputer", "meja",
        "kursi", "etalase", "timbangan", "kompor", "oven",
    ],
    "penjualan": [
        "penjualan", "order", "pelanggan", "jualan", "pembeli",
        "transaksi penjualan", "omzet", "cashier",
    ],
    "jasa": ["jasa", "service", "konsultasi", "desain jasa", "ongkos jasa"],
}

EXPENSE_CATEGORIES = ["bahan_baku", "operasional", "gaji", "pemasaran", "peralatan", "lainnya"]
INCOME_CATEGORIES = ["penjualan", "jasa", "lainnya"]


def categorize(note: str, txn_type: str) -> dict:
    """Categorize a transaction note.

    txn_type must be "pemasukan" or "pengeluaran".
    """
    lowered = f" {note.lower()} "
    allowed = INCOME_CATEGORIES if txn_type == "pemasukan" else EXPENSE_CATEGORIES
    for category, keywords in CATEGORY_KEYWORDS.items():
        if category not in allowed:
            continue
        for keyword in keywords:
            pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
            if re.search(pattern, lowered):
                return {"category": category, "confidence": 0.9, "matched_keyword": keyword}
    return {"category": "lainnya", "confidence": 0.3, "matched_keyword": None}
