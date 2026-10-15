"""Minimal command-line entrypoint to download and validate RTE data."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, date, datetime
from pathlib import Path

from gridpulse.ingestion.rte import fetch_range
from gridpulse.quality.rte import normalize


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and validate RTE demand records")
    parser.add_argument("--start", type=date.fromisoformat, required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", type=date.fromisoformat, required=True, help="Exclusive YYYY-MM-DD")
    parser.add_argument("--out", type=Path, default=Path("data"))
    args = parser.parse_args()
    if args.start >= args.end:
        parser.error("--end must be after --start (end is exclusive)")

    records = fetch_range(args.start, args.end)
    clean, quality = normalize(records)
    stem = f"rte_{args.start.isoformat()}_{args.end.isoformat()}"
    raw_dir = args.out / "raw"
    processed_dir = args.out / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_path = raw_dir / f"{stem}.jsonl"
    with raw_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    csv_path = processed_dir / f"{stem}.csv"
    fields = ["timestamp_utc", "demand_mw", "data_status", "source"]
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(clean)

    report = {
        "source": "RTE eco2mix-national-cons-def",
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "start_inclusive": args.start.isoformat(),
        "end_exclusive": args.end.isoformat(),
        "counts": quality,
        "raw_file": str(raw_path),
        "clean_file": str(csv_path),
    }
    report_path = processed_dir / f"{stem}_quality.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
