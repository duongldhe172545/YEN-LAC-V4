# Scenario 02 — Tier-3 Hard Stop (dừng khẩn)

## Trigger giả lập
- Metric: unconsented_pii_risk
- Điều kiện: >0 (ngưỡng tuyệt đối)

## Timeline (timebox 60 phút)
1) T+0: Field Runner báo Commander.
2) T+2: Commander kích hoạt Hard Stop (log-only).
3) T+5: Freeze payout + stop new jobs (quyết định war-room).
4) T+10: Bật Data Privacy Protocol: kiểm consent snapshot + xóa PII chưa consent.
5) T+30: Rollback drill (registry rollback) nếu cần.
6) T+60: Báo cáo HĐQT nếu chưa mở lại.

## PASS/FAIL
- PASS nếu: action đúng SLA + có bằng chứng xử lý consent/PII.
- FAIL nếu: vượt SLA hoặc không khóa payout.
