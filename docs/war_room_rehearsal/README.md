# War-room rehearsal kit (V5.0.2)

Mục tiêu: diễn tập trước go-live để **Tier-2 Throttle** và **Tier-3 Hard Stop** chạy đúng, kèm drill rollback.

## 3 kịch bản bắt buộc
1) Tier-2 Throttle: evidence_pass_rate giảm + payout_latency tăng.
2) Tier-3 Hard Stop: unconsented_pii_risk > 0 (ngưỡng tuyệt đối).
3) Data ingest sai: EVT batch lỗi → quarantine + registry rollback.

## Output cần ghi
- incident log (append-only)
- action log (ai làm gì, lúc nào)
- quyết định mở lại (decision log)
- AAR (After Action Review) trong 24h
