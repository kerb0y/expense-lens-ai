"""Command line interface for ExpenseLens AI.

Examples:
    python cli.py add --type pengeluaran --amount 50000 --note "beli beras supplier" --date 2026-10-27
    python cli.py list
    python cli.py summary
    python cli.py categorize --type pengeluaran --note "bayar listrik"
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.categorizer import categorize
from app.store import add_transaction, connect, list_transactions
from app.summary import summarize


def main() -> None:
    parser = argparse.ArgumentParser(prog="expense-lens", description="ExpenseLens AI CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Tambah transaksi")
    p_add.add_argument("--type", required=True, choices=["pemasukan", "pengeluaran"])
    p_add.add_argument("--amount", required=True, type=float)
    p_add.add_argument("--note", required=True)
    p_add.add_argument("--date", required=True)
    p_add.add_argument("--category", default=None)

    sub.add_parser("list", help="Tampilkan semua transaksi")
    sub.add_parser("summary", help="Tampilkan ringkasan keuangan")

    p_cat = sub.add_parser("categorize", help="Tebak kategori dari catatan")
    p_cat.add_argument("--type", required=True, choices=["pemasukan", "pengeluaran"])
    p_cat.add_argument("--note", required=True)

    args = parser.parse_args()
    conn = connect()
    try:
        if args.command == "add":
            category = args.category or categorize(args.note, args.type)["category"]
            result = add_transaction(
                conn,
                {
                    "type": args.type,
                    "amount": args.amount,
                    "category": category,
                    "note": args.note,
                    "date": args.date,
                },
            )
        elif args.command == "list":
            result = {"transactions": list_transactions(conn)}
        elif args.command == "summary":
            result = summarize(list_transactions(conn))
        else:
            result = categorize(args.note, args.type)
    finally:
        conn.close()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
