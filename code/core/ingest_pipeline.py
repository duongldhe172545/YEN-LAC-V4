"""P2-INGEST: Event ingest pipeline (nạp sự kiện) cho Pilot Yên Lạc.

Mục tiêu:
- Append-only (chỉ thêm, không sửa lịch sử): event_log.jsonl chỉ append.
- Idempotency (chống ghi trùng): dựa trên idempotency_key (khóa chống trùng).
- Registry-first (lấy registry làm chuẩn): validate theo registry/events.yaml.
- Quarantine (cách ly): bản ghi lỗi đi vào quarantine_events.jsonl, không làm gãy luồng.

Thuật ngữ:
- event: sự kiện (một việc đã xảy ra)
- ingest: nạp (đưa dữ liệu vào hệ thống)
- schema validation: kiểm tra khuôn/định dạng dữ liệu
- idempotency_key: khóa chống ghi trùng
- quarantine: cách ly bản ghi lỗi
"""

from __future__ import annotations

import csv
import json
import re
import uuid
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml


EVT_CODE_RE = re.compile(r"^EVT_[A-Z0-9_]+$")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_hash(values: List[str]) -> str:
    """Tạo hash ổn định cho idempotency_key từ list string."""
    h = hashlib.sha256()
    for v in values:
        h.update(v.encode("utf-8"))
        h.update(b"|")
    return h.hexdigest()


@dataclass(frozen=True)
class RegistryEventDef:
    event_code: str
    required_keys: List[str]
    evidence_required: bool
    idempotency_key_fields: List[str]


@dataclass
class IngestResult:
    accepted: int
    duplicated: int
    quarantined: int
    errors: List[str]


class EventRegistry:
    """Loader cho events registry (events.yaml)."""

    def __init__(self, defs: Dict[str, RegistryEventDef], aliases: Dict[str, str]):
        self.defs = defs
        self.aliases = aliases

    @staticmethod
    def load(repo_root: Path) -> "EventRegistry":
        p = repo_root / "registry" / "events.yaml"
        obj = yaml.safe_load(p.read_text(encoding="utf-8"))
        aliases = (obj.get("spec", {}) or {}).get("aliases", {}) or {}
        defs: Dict[str, RegistryEventDef] = {}
        for e in obj.get("events", []) or []:
            defs[e["event_code"]] = RegistryEventDef(
                event_code=e["event_code"],
                required_keys=list(e.get("required_keys", []) or []),
                evidence_required=bool(e.get("evidence_required", False)),
                idempotency_key_fields=list(e.get("idempotency_key_fields", []) or []),
            )
        return EventRegistry(defs=defs, aliases=aliases)

    def canonicalize_event_code(self, event_code: str) -> str:
        return self.aliases.get(event_code, event_code)

    def get(self, event_code: str) -> Optional[RegistryEventDef]:
        return self.defs.get(event_code)


def validate_event_record(
    rec: Dict[str, Any], reg: EventRegistry
) -> Tuple[bool, List[str], Optional[RegistryEventDef]]:
    """Validate record theo registry.

    Required fields tối thiểu (contract):
    - event_code
    - event_ts (ISO 8601)
    - idempotency_key (hoặc đủ idempotency_key_fields để tính)
    """
    errors: List[str] = []
    if "event_code" not in rec:
        errors.append("missing event_code")
        return False, errors, None

    raw_code = str(rec["event_code"]).strip()
    code = reg.canonicalize_event_code(raw_code)
    if not EVT_CODE_RE.match(code):
        errors.append(f"bad event_code format: {raw_code} -> {code}")
        return False, errors, None

    ev_def = reg.get(code)
    if ev_def is None:
        errors.append(f"unknown event_code: {code}")
        return False, errors, None

    # event_ts
    if "event_ts" not in rec or not str(rec["event_ts"]).strip():
        errors.append("missing event_ts")
    else:
        try:
            datetime.fromisoformat(str(rec["event_ts"]).replace("Z", "+00:00"))
        except Exception:
            errors.append(f"bad event_ts (expect ISO8601): {rec['event_ts']}")

    # required_keys theo event
    for k in ev_def.required_keys:
        if k not in rec or rec[k] in (None, ""):
            errors.append(f"missing required key: {k}")

    # idempotency
    if not rec.get("idempotency_key"):
        missing_fields = [f for f in ev_def.idempotency_key_fields if not rec.get(f)]
        if missing_fields:
            errors.append(
                "missing idempotency_key and missing idempotency_key_fields: "
                + ",".join(missing_fields)
            )

    return (len(errors) == 0), errors, ev_def


def compute_idempotency_key(rec: Dict[str, Any], ev_def: RegistryEventDef) -> str:
    """Tính idempotency_key nếu chưa có."""
    if rec.get("idempotency_key"):
        return str(rec["idempotency_key"])
    parts: List[str] = []
    for f in ev_def.idempotency_key_fields:
        parts.append(str(rec.get(f, "")))
    return stable_hash(parts)


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def load_idempotency_set(idx_path: Path, limit: int = 2_000_000) -> set[str]:
    """Load idempotency keys đã thấy trước đó."""
    s: set[str] = set()
    if not idx_path.exists():
        return s
    with idx_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            line = line.strip()
            if line:
                s.add(line)
    return s


def append_idempotency(idx_path: Path, key: str) -> None:
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    with idx_path.open("a", encoding="utf-8") as f:
        f.write(key + "\n")


def ingest_records(
    repo_root: Path,
    records: Iterable[Dict[str, Any]],
    source_batch_id: str,
    strip_unconsented_pii: bool = True,
) -> IngestResult:
    """Ingest nhiều record.

    Output (append-only):
    - data/event_store/event_log.jsonl
    - data/event_store/idempotency_keys.txt
    - data/quarantine/quarantine_events.jsonl
    - data/audit/ingest_audit.jsonl
    """
    reg = EventRegistry.load(repo_root)
    event_log = repo_root / "data" / "event_store" / "event_log.jsonl"
    idem_idx = repo_root / "data" / "event_store" / "idempotency_keys.txt"
    quarantine_log = repo_root / "data" / "quarantine" / "quarantine_events.jsonl"
    audit_log = repo_root / "data" / "audit" / "ingest_audit.jsonl"

    seen = load_idempotency_set(idem_idx)

    accepted = duplicated = quarantined = 0
    errors: List[str] = []

    for rec in records:
        if "event_code" in rec:
            rec["event_code"] = reg.canonicalize_event_code(str(rec["event_code"]).strip())

        ok, errs, ev_def = validate_event_record(rec, reg)
        if not ok or ev_def is None:
            quarantined += 1
            append_jsonl(
                quarantine_log,
                {
                    "ingest_ts": utc_now_iso(),
                    "source_batch_id": source_batch_id,
                    "reason": "schema_validation_failed",
                    "errors": errs,
                    "record": rec,
                },
            )
            continue

        rec["idempotency_key"] = compute_idempotency_key(rec, ev_def)
        idem_key = f"{rec['event_code']}|{rec['idempotency_key']}"
        if idem_key in seen:
            duplicated += 1
            continue

        # Consent/PII: nếu consent_flag==False thì không lưu pii_* (tối thiểu)
        if strip_unconsented_pii:
            consent_flag = rec.get("consent_flag")
            if consent_flag is False:
                for k in [k for k in list(rec.keys()) if k.lower().startswith("pii_")]:
                    rec.pop(k, None)

        event_obj = {
            "event_log_id": str(uuid.uuid4()),
            "ingest_ts": utc_now_iso(),
            "source_batch_id": source_batch_id,
            "event_code": rec["event_code"],
            "event_ts": rec["event_ts"],
            "idempotency_key": rec["idempotency_key"],
            "payload": {k: v for k, v in rec.items() if k not in ("event_code", "event_ts", "idempotency_key")},
        }

        append_jsonl(event_log, event_obj)
        append_idempotency(idem_idx, idem_key)
        seen.add(idem_key)
        accepted += 1

    append_jsonl(
        audit_log,
        {
            "ingest_ts": utc_now_iso(),
            "source_batch_id": source_batch_id,
            "accepted": accepted,
            "duplicated": duplicated,
            "quarantined": quarantined,
        },
    )

    return IngestResult(
        accepted=accepted, duplicated=duplicated, quarantined=quarantined, errors=errors
    )


def read_csv_events(path: Path) -> List[Dict[str, Any]]:
    """Đọc CSV thành list record. Nếu có cột payload_json thì parse JSON."""
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rec: Dict[str, Any] = {k: (v if v != "" else None) for k, v in r.items()}
            if rec.get("payload_json"):
                try:
                    payload = json.loads(str(rec["payload_json"]))
                    if isinstance(payload, dict):
                        rec.update(payload)
                except Exception:
                    pass
            rows.append(rec)
    return rows
