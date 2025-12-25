#!/usr/bin/env python3
"""
demo_kpi_pulse.py – KPI pulse tối giản để chạy thử (không thay SSOT).

English → Việt:
- KPI (Key Performance Indicator): chỉ số đo hiệu suất
- pulse: bản chụp nhanh (snapshot) theo thời điểm
- state machine: máy trạng thái (chuỗi trạng thái)
"""

import argparse, json
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml


STATE_ORDER = ["SHADOW","QUALIFIED","CLAIMED","FINANCIAL","GOLDEN"]


def load_events_registry(repo_root: Path):
    obj = yaml.safe_load((repo_root/"registry"/"events.yaml").read_text(encoding="utf-8"))
    out = {}
    for e in obj.get("events", []):
        code = e["event_code"]
        si = e.get("state_impact") or {}
        to_state = None
        if isinstance(si, dict):
            # format 1: {"to_state": "..."}
            if "to_state" in si:
                to_state = si.get("to_state")
            # format 2: {"house_lifecycle": {"from": "...", "to": "QUALIFIED"}}
            elif isinstance(si.get("house_lifecycle"), dict):
                to_state = si["house_lifecycle"].get("to")
        out[code] = to_state
    return out


def read_event_log(path: Path):
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def iso_to_dt(s: str):
    return datetime.fromisoformat(s.replace("Z","+00:00"))


def get_field(e: dict, k: str):
    if k in e and e.get(k) is not None:
        return e.get(k)
    payload = e.get("payload") or {}
    return payload.get(k)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo_root", required=True)
    ap.add_argument("--event_log", default="data/event_store/event_log.jsonl")
    ap.add_argument("--out", default="data/kpi_pulse/kpi_pulse.json")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    event_log_path = (repo_root / args.event_log).resolve()

    to_state_map = load_events_registry(repo_root)
    events = read_event_log(event_log_path)

    per_code = Counter([e.get("event_code") for e in events])
    houses = set([get_field(e, "house_id") for e in events if get_field(e, "house_id")])

    # compute latest state per house by event_ts order
    latest_state = {h:"SHADOW" for h in houses}
    events_sorted = sorted([e for e in events if e.get("event_ts")], key=lambda x: iso_to_dt(x["event_ts"]))
    for e in events_sorted:
        hid = get_field(e, "house_id")
        if not hid:
            continue
        ts = to_state_map.get(e.get("event_code"))
        if ts in STATE_ORDER:
            latest_state[hid] = ts

    state_counts = Counter(latest_state.values())

    out_obj = {
        "generated_at": datetime.utcnow().isoformat()+"Z",
        "accepted_events": len(events),
        "unique_house_count": len(houses),
        "events_by_code": dict(per_code),
        "house_state_counts": dict(state_counts),
    }

    out_path = (repo_root / args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out_obj, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(out_obj, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
