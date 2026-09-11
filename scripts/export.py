"""Export a per-product revenue report.

Usage (see README):  uv run python export.py
"""

import csv
from collections import defaultdict
from pathlib import Path

DATA = Path("data/raw/sales_2024.csv")
OUT = Path("../report.csv")   # one level up, so the report lands next to the project folder


def main() -> None:
    revenue = defaultdict(float)
    with DATA.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            revenue[row["product"]] += int(row["units"]) * float(row["unit_price"])
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["product", "revenue"])
        for product in sorted(revenue):
            w.writerow([product, f"{revenue[product]:.2f}"])
    print(f"wrote {OUT.resolve()}")


if __name__ == "__main__":
    main()
