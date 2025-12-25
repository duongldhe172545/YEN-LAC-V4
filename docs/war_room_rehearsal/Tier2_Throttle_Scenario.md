# Scenario: Tier-2 Throttle (V5.0.2)

## Trigger
- metric_code: evidence_pass_rate
- condition: < 0.85 (PROVISIONAL)
- action_tier: 2

## Timeline (timebox 30 phút)
1) T+0: Gate Monitor đỏ/vàng → Field Runner mở incident.
2) T+5m: Ops Lead bật throttle_new_jobs + quarantine_scope job/house.
3) T+10m: Data Lead xác minh evidence integrity (hash/exif/geo) + kiểm alias drift.
4) T+20m: Finance Controller freeze payout theo điều kiện (conditional).
5) T+30m: quyết định mở lại hoặc nâng Tier-3.

## Pass criteria
- Throttle thực thi trong 30 phút.
- Quarantine queue có record đầy đủ (metric_code/entity/entity_id/reason).
- Log append-only không bị sửa.
