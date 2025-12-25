#!/usr/bin/env python3
"""
demo_scenario.py – mô phỏng kịch bản (Scenario) tối giản để chạy thử.

English → Việt:
- scenario: kịch bản (tập giả định)
- threshold: ngưỡng (mốc cảnh báo)
- kill-switch: cầu dao ngắt (ngắt vận hành khi rủi ro)
"""

import argparse, json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import yaml


def load_thresholds(repo_root: Path):
    p = repo_root / "registry" / "thresholds.yaml"
    if not p.exists():
        return []
    obj = yaml.safe_load(p.read_text(encoding="utf-8"))
    return obj.get("thresholds", []) or []


def decide_simple(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule demo (không coi là luật sản xuất):
    - Unconsented_PII_Risk > 0 => Tier_3_Hard_Stop
    - evidence_pass_rate < 0.80 => Tier_2_Throttle
    - evidence_pass_rate < 0.90 => Tier_1_Warning
    """
    decisions = []
    # 1) PII kill-switch
    if float(params.get("unconsented_pii_risk", 0) or 0) > 0:
        decisions.append({"metric_code":"unconsented_pii_risk","tier":"Tier_3_Hard_Stop","reason":"PII chưa consent (không được lưu/không được chạy)."})
    # 2) Evidence pass rate
    epr = params.get("evidence_pass_rate")
    if epr is not None:
        epr = float(epr)
        if epr < 0.80:
            decisions.append({"metric_code":"evidence_pass_rate","tier":"Tier_2_Throttle","reason":"Bằng chứng fail nhiều, cần giảm tốc + soi lỗi."})
        elif epr < 0.90:
            decisions.append({"metric_code":"evidence_pass_rate","tier":"Tier_1_Warning","reason":"Cảnh báo chất lượng bằng chứng."})
    if not decisions:
        decisions.append({"tier":"OK","reason":"Không chạm ngưỡng demo."})
    return {"decisions": decisions}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo_root", required=True)
    ap.add_argument("--input_json", required=True, help="file chứa list scenario params")
    ap.add_argument("--out", default="data/scenario/scenario_results.json")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    scenarios = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    out = []
    thresholds = load_thresholds(repo_root)  # currently unused in demo

    for sc in scenarios:
        params = sc.get("params", {})
        res = decide_simple(params)
        out.append({
            "scenario_id": sc.get("scenario_id"),
            "name": sc.get("name"),
            "params": params,
            "result": res,
            "generated_at": datetime.utcnow().isoformat()+"Z",
        })

    out_path = (repo_root / args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
