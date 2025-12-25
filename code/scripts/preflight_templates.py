"""
Preflight Templates – soi lỗi trước khi ingest (chạy cơm → chạy máy).

Mục tiêu:
- Kiểm lỗi "thô" trước khi nạp: thiếu khóa, duplicate, format thời gian, số.
- Không thay đổi SSOT: chỉ tạo report ở data/preflight/ (append-only output).

Thuật ngữ:
- preflight (soi lỗi trước khi nạp)
- ingest (nạp)
- schema (khuôn dữ liệu)
- append-only (chỉ thêm, không sửa lịch sử)
- idempotency_key (khóa chống ghi trùng)
- quarantine (cách ly bản ghi lỗi)
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


@dataclass
class PreflightSummary:
    total: int
    passed: int
    failed: int
    duplicates: int


def utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def load_schema(repo_root: Path, template_code: str) -> Dict[str, Any]:
    """Load schema YAML by template_code from templates/schema_generated/."""
    schema_dir = repo_root / "templates" / "schema_generated"
    if not schema_dir.exists():
        raise SystemExit("missing templates/schema_generated/. Bạn chưa có schema_generated trong repo.")
    # 1) exact match by internal template_code
    for p in schema_dir.glob("*.schema.yaml"):
        obj = yaml.safe_load(p.read_text(encoding="utf-8"))
        if str(obj.get("template_code", "")).strip() == template_code:
            return obj
    # 2) fallback by filename contains template_code
    cand = list(schema_dir.glob(f"*{template_code}*.schema.yaml"))
    if cand:
        return yaml.safe_load(cand[0].read_text(encoding="utf-8"))
    raise SystemExit(f"schema not found for template_code={template_code}")


def read_csv_rows(path: Path) -> Tuple[List[str], List[Dict[str, Any]]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols = list(reader.fieldnames or [])
        for r in reader:
            rows.append({k: (v if v != "" else None) for k, v in r.items()})
    return cols, rows


def is_iso8601(s: str) -> bool:
    try:
        datetime.fromisoformat(s.replace("Z", "+00:00"))
        return True
    except Exception:
        return False


def validate_rows(schema: Dict[str, Any], cols: List[str], rows: List[Dict[str, Any]]) -> Tuple[PreflightSummary, List[Dict[str, Any]]]:
    template_code = str(schema.get("template_code"))
    pk = list(schema.get("primary_key", []) or [])
    stage = str(schema.get("stage", "")).upper()

    # required = primary_key + (event_code,event_ts) nếu là event template
    required = list(pk)
    is_events = "EVENT" in template_code.upper() or template_code.upper().startswith("A7_")
    if is_events:
        for c in ["event_code", "event_ts", "idempotency_key"]:
            if c not in required:
                required.append(c)

    # duplicate key
    def dup_key(r: Dict[str, Any]) -> str:
        if is_events:
            return f"{r.get('event_code')}|{r.get('idempotency_key')}"
        return "|".join(str(r.get(k, "")) for k in pk)

    seen = set()
    results: List[Dict[str, Any]] = []
    passed = failed = duplicates = 0

    for idx, r in enumerate(rows, start=1):
        errs: List[str] = []

        for c in required:
            if r.get(c) in (None, ""):
                errs.append(f"missing_required:{c}")

        dk = dup_key(r)
        if dk in seen:
            duplicates += 1
            errs.append("duplicate_key")
        else:
            seen.add(dk)

        # time fields basic check
        for c in cols:
            if c.endswith("_ts") or c in ("event_ts", "capture_ts"):
                v = r.get(c)
                if v not in (None, "") and not is_iso8601(str(v)):
                    errs.append(f"bad_iso8601:{c}")

        # numeric sanity (very light)
        for c in ["lat", "lng", "roof_area_m2"]:
            if c in cols and r.get(c) not in (None, ""):
                try:
                    float(str(r.get(c)))
                except Exception:
                    errs.append(f"bad_number:{c}")

        ok = len(errs) == 0
        if ok:
            passed += 1
        else:
            failed += 1

        results.append({"row_index": idx, "template_code": template_code, "ok": ok, "errors": errs, "row": r})

    return PreflightSummary(total=len(rows), passed=passed, failed=failed, duplicates=duplicates), results


def write_report(repo_root: Path, template_code: str, summary: PreflightSummary, results: List[Dict[str, Any]]) -> Path:
    out_dir = repo_root / "data" / "preflight"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"preflight_{template_code}_{ts}.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"type":"summary","ingest_ts":utc_now_iso(),"template_code":template_code,"summary":summary.__dict__}, ensure_ascii=False) + "\n")
        for obj in results:
            f.write(json.dumps({"type":"row", **obj}, ensure_ascii=False) + "\n")
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo_root", required=True)
    ap.add_argument("--template_code", required=True, help="Ví dụ: A7_events_evt_star hoặc A1_house_master")
    ap.add_argument("--input_csv", required=True)
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    schema = load_schema(repo_root, args.template_code)
    cols, rows = read_csv_rows(Path(args.input_csv).resolve())
    summary, results = validate_rows(schema, cols, rows)
    report = write_report(repo_root, schema["template_code"], summary, results)

    print(f"template_code={schema['template_code']} total={summary.total} passed={summary.passed} failed={summary.failed} duplicates={summary.duplicates}")
    print(f"report={report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
