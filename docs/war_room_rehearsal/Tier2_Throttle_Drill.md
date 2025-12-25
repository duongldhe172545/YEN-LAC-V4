# Scenario A — Tier 2 Throttle (30 phút)

## Trigger (giả lập)
- Metric: `pending_consent_aging_hours` hoặc `payout_latency_hours`
- Condition: vượt ngưỡng Tier 2 trong `registry/thresholds.yaml`

## Expected actions (theo runbook_actions.yaml)
- Ops Lead: throttle_new_jobs=true
- Finance Controller: throttle_payout=conditional
- Data Lead: mở quarantine_scope = [job, house]

## Pass/Fail
PASS nếu:
- 5 phút có thông báo + incident opened
- 30 phút có throttle thực thi (log + quyết định)
- Có root cause note tối thiểu 3 dòng
