# Dataset split utility

from __future__ import annotations

import csv
import json
from pathlib import Path


def split_dataset(csv_path: str | Path, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise ValueError("The dataset CSV is empty.")

    train = rows[: int(len(rows) * 0.7)]
    val = rows[int(len(rows) * 0.7): int(len(rows) * 0.85)]
    test = rows[int(len(rows) * 0.85):]

    for name, items in {"train": train, "val": val, "test": test}.items():
        with (output_dir / f"{name}.json").open("w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)

    print(f"Split complete. Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split a CSV dataset into train/validation/test files.")
    parser.add_argument("csv_path", help="Path to the dataset CSV with image and age columns.")
    parser.add_argument("output_dir", help="Directory for the split JSON files.")
    args = parser.parse_args()
    split_dataset(args.csv_path, args.output_dir)
