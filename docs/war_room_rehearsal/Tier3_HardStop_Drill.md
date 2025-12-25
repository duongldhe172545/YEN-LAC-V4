# Scenario B — Tier 3 Hard Stop (25 phút)

## Trigger (giả lập)
- Metric: `unconsented_pii_risk`
- Condition: > 0 (LOCKED) ⇒ Hard Stop ngay

## Expected actions
- Commander: stop_new_jobs=true + board_update
- Finance Controller: freeze_payout=true (đóng van tiền)
- Data Lead: activate_data_privacy_protocol=true (xóa/không lưu PII khi chưa consent)
- Field Runner: cách ly hiện trường, thu bằng chứng...

## Pass/Fail
- Pass nếu: từ lúc trigger đến freeze payout + stop jobs <= 15 phút (action_time Tier 3)
- Fail nếu: không rõ owner, hoặc không tạo incident log + quarantine log
