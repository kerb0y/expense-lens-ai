# ExpenseLens AI

Aplikasi pencatatan keuangan untuk UMKM kecil yang tidak mau ribet dengan spreadsheet. Pengguna cukup menulis catatan transaksi dalam bahasa sehari-hari, misalnya "beli beras supplier" atau "bayar listrik toko", sistem menebak kategorinya secara otomatis, dan ringkasan pemasukan, pengeluaran, serta laba dihitung langsung.

Project ini dibuat sebagai project mingguan kedua setelah CV Lens AI, dengan fokus yang berbeda: bukan lagi analisis dokumen, melainkan produk harian yang bisa langsung dipakai pemilik usaha kecil. Datanya disimpan lokal di SQLite, jadi tidak butuh server database dan tidak butuh API key berbayar.

## Fitur Utama

- Tambah, lihat, dan hapus transaksi pemasukan dan pengeluaran
- Kategorisasi otomatis berbasis aturan kata kunci yang transparan, dengan confidence yang jujur: cocok kata kunci berarti 0.9, tidak cocok berarti 0.3 dan masuk "lainnya"
- Ringkasan otomatis: total pemasukan, total pengeluaran, laba, total per kategori, dan total per bulan
- Halaman web sederhana tanpa build step, cukup buka setelah server jalan
- CLI untuk pemakaian cepat dari terminal
- API REST lengkap dengan dokumentasi interaktif di /docs

## Kategori yang Didukung

Pengeluaran: bahan_baku, operasional, gaji, pemasaran, peralatan, lainnya.
Pemasukan: penjualan, jasa, lainnya.

Daftar kata kunci ada di `app/categorizer.py` dan mudah diubah sesuai jenis usaha. Misalnya warung makan akan banyak memakai bahan_baku dan operasional, sementara jasa desain akan banyak memakai jasa dan pemasaran.

## Menjalankan Project

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Buka http://127.0.0.1:8000/ untuk aplikasi web, dan http://127.0.0.1:8000/docs untuk dokumentasi API.

## Memakai CLI

```bash
python cli.py add --type pengeluaran --amount 50000 --note "beli beras supplier" --date 2026-10-27
python cli.py list
python cli.py summary
python cli.py categorize --type pengeluaran --note "bayar listrik"
```

Contoh hasil dari data contoh di `examples/sample_transactions.csv`:

- Total pemasukan: Rp 370.000
- Total pengeluaran: Rp 280.000
- Laba: Rp 90.000

Perhitungan ini berasal dari 5 baris contoh tersebut: pemasukan 250.000 plus 120.000, pengeluaran 50.000 plus 150.000 plus 80.000.

## Endpoint API

| Method | Endpoint | Fungsi |
| --- | --- | --- |
| GET | / | Halaman web aplikasi |
| GET | /health | Cek status server |
| POST | /api/categorize | Tebak kategori dari catatan |
| POST | /api/transactions | Tambah transaksi, kategori otomatis jika kosong |
| GET | /api/transactions | Daftar transaksi, bisa difilter type dan category |
| GET | /api/summary | Ringkasan keuangan |
| DELETE | /api/transactions/{id} | Hapus transaksi |

## Struktur Project

```
app/
  main.py         Aplikasi FastAPI
  schemas.py      Skema request
  store.py        Penyimpanan SQLite
  categorizer.py  Aturan kategorisasi berbasis kata kunci
  summary.py      Agregasi ringkasan keuangan
frontend/
  index.html      Halaman web tanpa build step
cli.py            Antarmuka command line
examples/         Contoh data transaksi
tests/            Unit test dan test API
```

## Menjalankan Test

```bash
pytest -q
```

## Roadmap

- Impor transaksi dari file CSV
- Ekspor laporan bulanan ke CSV dan PDF
- Grafik per kategori dan per bulan di halaman web
- Belajar kategori dari koreksi pengguna, bukan hanya aturan kata kunci
- Mode multi usaha untuk satu akun

## Potensi Penggunaan

Aplikasi ini bisa ditawarkan sebagai jasa setup pencatatan keuangan untuk warung, toko, dan jasa kecil, dengan biaya setup satu kali plus pendampingan bulanan. Versi berikutnya bisa dikembangkan menjadi SaaS pencatatan keuangan UMKM dengan harga langganan ringan.

## Author

**Ade Bintang**

Mahasiswa Informatika Universitas Gunadarma dengan fokus pada AI Engineering dan Data Science.

GitHub: [@kerb0y](https://github.com/kerb0y)

## License

MIT License. Lihat file LICENSE untuk detailnya.
