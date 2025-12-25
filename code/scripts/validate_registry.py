#!/usr/bin/env python3
"""validate_registry.py — Lint registry theo V5.0.2 (Yên Lạc)

Usage:
  python code/scripts/validate_registry.py --repo_root .

Exit code:
  0 = PASS
  1 = FAIL (FATAL)

Nguyên tắc:
- FAIL khi vi phạm invariants (FATAL).
- WARN khi thiếu dữ liệu/placeholder (khuyến nghị bổ sung).

Invariants (khóa drift):
- event_code phải match ^EVT_[A-Z0-9_]+$
- house_lifecycle_status phải thuộc {SHADOW,QUALIFIED,CLAIMED,FINANCIAL,GOLDEN}
- thresholds.metric_code phải tồn tại trong metrics.csv (hoặc là alias hợp lệ)
- threshold rule phải có action_tier ∈ {1,2,3} và tier name nằm trong {TIER_1_WARNING,TIER_2_THROTTLE,TIER_3_HARD_STOP}
- metric kill_switch=true phải có ít nhất 1 rule TIER_3_HARD_STOP

Lưu ý:
- Đây là lint "kỹ thuật" để CI chặn drift, không thay thế review nghiệp vụ.
"""

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

HOUSE_LIFECYCLE = {"SHADOW", "QUALIFIED", "CLAIMED", "FINANCIAL", "GOLDEN"}
EVT_PAT = re.compile(r"^EVT_[A-Z0-9_]+$")
TIER_NAMES = {"TIER_1_WARNING", "TIER_2_THROTTLE", "TIER_3_HARD_STOP"}
VALID_ACTION_TIERS = {1, 2, 3}


def fatal(msg: str) -> None:
    print(f"FATAL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def warn(msg: str) -> None:
    print(f"WARN: {msg}", file=sys.stderr)


def load_yaml(path: Path):
    try:
        import yaml
    except Exception:
        fatal("PyYAML not installed. Install pyyaml to run validator.")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_metrics_csv(path: Path) -> Tuple[Set[str], Dict[str, bool]]:
    """Return (metric_codes, kill_switch_map)."""
    metric_codes: Set[str] = set()
    kill_switch: Dict[str, bool] = {}

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            fatal("metrics.csv has no header")
        required = {"metric_code", "unit", "window"}
        missing = required - set(reader.fieldnames)
        if missing:
            fatal(f"metrics.csv missing columns: {sorted(missing)}")

        for row in reader:
            code = (row.get("metric_code") or "").strip()
            if not code:
                fatal("metrics.csv contains empty metric_code")
            if code in metric_codes:
                fatal(f"Duplicate metric_code in metrics.csv: {code}")
            metric_codes.add(code)

            ks_raw = (row.get("kill_switch") or "").strip().lower()
            ks = ks_raw in {"true", "1", "yes", "y"}
            kill_switch[code] = ks

    return metric_codes, kill_switch


def load_metric_alias(path: Path) -> Dict[str, str]:
    """Return alias -> canonical map."""
    alias_map: Dict[str, str] = {}
    if not path.exists():
        return alias_map

    obj = load_yaml(path) or {}

    # Accept either:
    # 1) {aliases: {alias: canonical}}
    # 2) {canonical_to_aliases: {canonical: [alias...]}}
    if isinstance(obj, dict) and "aliases" in obj and isinstance(obj["aliases"], dict):
        for a, c in obj["aliases"].items():
            if not a or not c:
                continue
            alias_map[str(a)] = str(c)
        return alias_map

    canonical_to_aliases = obj.get("canonical_to_aliases") if isinstance(obj, dict) else None
    if canonical_to_aliases is None and isinstance(obj, dict):
        canonical_to_aliases = obj

    if isinstance(canonical_to_aliases, dict):
        for canonical, aliases in canonical_to_aliases.items():
            if not isinstance(aliases, list):
                continue
            for a in aliases:
                if not a:
                    continue
                a = str(a)
                canonical = str(canonical)
                if a in alias_map and alias_map[a] != canonical:
                    fatal(f"Alias collision: '{a}' maps to both {alias_map[a]} and {canonical}")
                alias_map[a] = canonical

    return alias_map


def lint_events(events_path: Path) -> None:
    data = load_yaml(events_path)
    if not isinstance(data, dict) or "events" not in data:
        fatal("events.yaml must be a dict with top-level key 'events'")

    ev_list = data.get("events")
    if not isinstance(ev_list, list) or len(ev_list) == 0:
        fatal("events.yaml has no events")

    for ev in ev_list:
        code = ev.get("event_code")
        if not code:
            fatal("An event is missing event_code")
        if not EVT_PAT.match(code):
            fatal(f"Bad event_code '{code}' (must match EVT_[A-Z0-9_]+)")

        # required_keys must exist and be list
        rk = ev.get("required_keys")
        if not isinstance(rk, list) or len(rk) == 0:
            fatal(f"{code}: required_keys must be non-empty list")

        # payload_required should be list (can be empty but warn)
        pr = ev.get("payload_required")
        if pr is None:
            warn(f"{code}: payload_required missing (recommended even if empty list)")
        elif not isinstance(pr, list):
            fatal(f"{code}: payload_required must be a list")

        # evidence_required for monetary_impact events
        mi = bool(ev.get("monetary_impact", False))
        er = ev.get("evidence_required")
        if mi and (not isinstance(er, list) or len(er) == 0):
            fatal(f"{code}: monetary_impact=true requires non-empty evidence_required")

        # state_impact house_lifecycle to must be uppercase enum
        si = ev.get("state_impact") or {}
        hl = (si.get("house_lifecycle") or {}) if isinstance(si, dict) else {}
        to_state = hl.get("to")
        if to_state is not None:
            if str(to_state).upper() != str(to_state):
                fatal(f"{code}: house_lifecycle.to must be UPPERCASE (got '{to_state}')")
            if to_state not in HOUSE_LIFECYCLE:
                fatal(f"{code}: house_lifecycle.to invalid '{to_state}'")

        # idempotency_key_fields recommended
        idem = ev.get("idempotency_key_fields")
        if not isinstance(idem, list) or len(idem) == 0:
            warn(f"{code}: missing/empty idempotency_key_fields (recommended)")


def lint_thresholds(
    thresholds_path: Path,
    metric_codes: Set[str],
    kill_switch_map: Dict[str, bool],
    alias_map: Dict[str, str],
) -> None:
    data = load_yaml(thresholds_path)
    if not isinstance(data, dict) or "thresholds" not in data:
        fatal("thresholds.yaml must be a dict with top-level key 'thresholds'")

    items = data.get("thresholds")
    if not isinstance(items, list) or len(items) == 0:
        fatal("thresholds.yaml has no thresholds")

    # Build helper
    def canonical_metric(code: str) -> str:
        return alias_map.get(code, code)

    for t in items:
        m = t.get("metric_code")
        if not m:
            fatal("A threshold entry is missing metric_code")
        m_can = canonical_metric(m)
        if m_can not in metric_codes:
            fatal(f"threshold metric_code '{m}' not found in metrics.csv (canonical '{m_can}')")

        tiers = t.get("tiers")
        if not isinstance(tiers, list) or len(tiers) == 0:
            fatal(f"{m}: tiers must be non-empty list")

        seen_tier_names: Set[str] = set()
        has_t3 = False
        for rule in tiers:
            tn = rule.get("tier")
            if tn not in TIER_NAMES:
                fatal(f"{m}: invalid tier name '{tn}'")
            if tn in seen_tier_names:
                fatal(f"{m}: duplicate tier '{tn}'")
            seen_tier_names.add(tn)
            if tn == "TIER_3_HARD_STOP":
                has_t3 = True

            at = rule.get("action_tier")
            try:
                at_int = int(at)
            except Exception:
                fatal(f"{m}: action_tier must be int 1/2/3 (got '{at}')")
            if at_int not in VALID_ACTION_TIERS:
                fatal(f"{m}: action_tier must be in {sorted(VALID_ACTION_TIERS)}")

            cond = rule.get("condition")
            if not isinstance(cond, dict):
                fatal(f"{m}/{tn}: condition must be dict")
            op = cond.get("op")
            if op not in {">", ">=", "<", "<=", "=="}:
                fatal(f"{m}/{tn}: unsupported op '{op}'")
            if ("value" not in cond) and ("value_ref" not in cond):
                fatal(f"{m}/{tn}: condition.value missing (or value_ref)")
            if "value_ref" in cond:
                vr = cond.get("value_ref")
                if not isinstance(vr, dict):
                    fatal(f"{m}/{tn}: condition.value_ref must be dict")
                ref_mc = vr.get("metric_code")
                if not isinstance(ref_mc, str) or not ref_mc.strip():
                    fatal(f"{m}/{tn}: value_ref.metric_code missing")
                mult = vr.get("multiplier", 1.0)
                try:
                    float(mult)
                except Exception:
                    fatal(f"{m}/{tn}: value_ref.multiplier must be numeric")

        ks_metric = bool(kill_switch_map.get(m_can, False)) or bool(t.get("kill_switch", False))
        if ks_metric and not has_t3:
            fatal(f"{m}: kill_switch=true requires a TIER_3_HARD_STOP rule")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo_root", default=".")
    args = ap.parse_args()
    root = Path(args.repo_root)

    reg = root / "registry"
    events_path = reg / "events.yaml"
    metrics_path = reg / "metrics.csv"
    alias_path = reg / "metric_alias.yaml"
    thresholds_path = reg / "thresholds.yaml"

    for p in [events_path, metrics_path, thresholds_path]:
        if not p.exists():
            fatal(f"Missing required file: {p}")

    metric_codes, kill_switch_map = load_metrics_csv(metrics_path)
    alias_map = load_metric_alias(alias_path)

    # Alias canonical must exist
    for a, c in alias_map.items():
        if c not in metric_codes:
            warn(f"alias '{a}' -> canonical '{c}' not found in metrics.csv")

    lint_events(events_path)
    lint_thresholds(thresholds_path, metric_codes, kill_switch_map, alias_map)

    print("PASS: registry lint ok")


if __name__ == "__main__":
    main()
