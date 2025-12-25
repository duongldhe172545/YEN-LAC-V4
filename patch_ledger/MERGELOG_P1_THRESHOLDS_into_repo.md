# MERGELOG — P1-THRESHOLDS into repo (V5.0.2)

## Copy operations (append-only)
1) Copy `thresholds.yaml` → `d2com-pilot-yen-lac/registry/thresholds.yaml` (replace placeholder).
2) Copy `P1-THRESHOLDS_v5_0_2_2025-12-24.md` → `d2com-pilot-yen-lac/patch_ledger/`
3) Append nội dung `patch_decision_log_append.md` vào cuối `d2com-pilot-yen-lac/patch_ledger/patch_decision_log.md`
   - Nếu file decision log chưa tồn tại: tạo mới và paste nội dung append vào.

## Post-merge checks
- YAML parse ok
- Join-check metric_code ∈ metrics.csv
- Kill-check: kill_switch metrics có TIER_3_HARD_STOP
- Action-check: action_tier ∈ runbook_actions.yaml.kill_switch_tiers
