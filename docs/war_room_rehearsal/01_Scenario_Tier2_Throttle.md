# Scenario 01 — Tier-2 Throttle (siết)

## Trigger giả lập
- Metric: payout_latency_hours hoặc evidence_pass_rate
- Điều kiện: vượt ngưỡng Tier-2 theo thresholds.yaml

## Timeline (timebox 30 phút)
1) T+0: Alert -> Field Runner mở incident.
2) T+5: Ops Lead kích hoạt Throttle (log-only trong Kill-switch Panel).
3) T+10: Quarantine scope: job/house (append case vào quarantine queue).
4) T+20: Update Commander + Finance Controller.
5) T+30: Root cause note + quyết định tiếp tục siết/khôi phục.

## PASS/FAIL
- PASS nếu: log đầy đủ + quarantine có record + có note nguyên nhân.
- FAIL nếu: không ai nhận trách nhiệm/không có log/không quarantine.
