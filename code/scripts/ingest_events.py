"""CLI cho P2-INGEST (nạp sự kiện)

Chạy từ repo root:
  python code/scripts/ingest_events.py --repo_root . --input_csv demo_inputs/events/events_demo.csv

English → Việt:
- ingest: nạp dữ liệu
- registry-first: sổ chuẩn trước, code đọc sổ
- append-only: chỉ thêm, không sửa lịch sử
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Ensure imports work when running as a script from repo root.
# Add repo_root/code to PYTHONPATH.
CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from core.ingest_pipeline import ingest_records, read_csv_events


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo_root", required=True, help="Đường dẫn repo root (chứa registry/)")
    ap.add_argument("--input_csv", required=True, help="CSV input events")
    ap.add_argument(
        "--source_batch_id",
        default=None,
        help="Mã batch nguồn (ví dụ: VDCD_20251224_001)",
    )
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    input_csv = Path(args.input_csv).resolve()

    source_batch_id = args.source_batch_id or f"BATCH_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

    records = read_csv_events(input_csv)
    res = ingest_records(repo_root=repo_root, records=records, source_batch_id=source_batch_id)

    print(f"accepted={res.accepted} duplicated={res.duplicated} quarantined={res.quarantined}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
