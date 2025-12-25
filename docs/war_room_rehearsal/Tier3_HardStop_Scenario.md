# Scenario: Tier-3 Hard Stop (V5.0.2)

## Trigger (tuyệt đối)
- metric_code: unconsented_pii_risk
- condition: > 0
- action_tier: 3

## Timeline (timebox 15 phút)
1) T+0: COMMANDER kích Hard Stop (stop_new_jobs, freeze_payout).
2) T+2m: Data Privacy Protocol bật (cô lập dữ liệu nghi ngờ, khoá export).
3) T+5m: Data Lead xác định phạm vi vi phạm (house/job/batch).
4) T+10m: Rollback nếu do registry drift/bug.
5) T+15m: thông báo HĐQT nếu chưa mở lại.

## Pass criteria
- Freeze payout trong 15 phút.
- Quarantine toàn bộ scope.
- Có decision log "re-open" hoặc "continue stop".
