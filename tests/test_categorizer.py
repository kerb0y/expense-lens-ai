import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.categorizer import categorize


def test_bahan_baku():
    assert categorize("beli beras supplier", "pengeluaran")["category"] == "bahan_baku"


def test_operasional():
    assert categorize("bayar listrik toko", "pengeluaran")["category"] == "operasional"


def test_gaji():
    assert categorize("gaji pegawai bulan ini", "pengeluaran")["category"] == "gaji"


def test_penjualan():
    assert categorize("penjualan hari ini pelanggan toko", "pemasukan")["category"] == "penjualan"


def test_unknown_falls_back():
    result = categorize("sesuatu yang tidak jelas sama sekali xyz", "pengeluaran")
    assert result["category"] == "lainnya"
    assert result["confidence"] < 0.5
