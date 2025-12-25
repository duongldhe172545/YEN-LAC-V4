# Rollback Procedures (P1-ROLLBACK)

SSOT: `governance/rollback_procedures.yaml`

## Khi nào rollback?
- Registry drift (alias collision, thresholds sai tier) → rollback registry.
- Bug chạm payout/fraud/consent → rollback code.
- Ingest batch sai → rollback data.

## Nguyên tắc
- Rollback là hành động **append-only**: phải log lại vào `audit/kill_switch_log.jsonl` hoặc `audit/quarantine_queue.jsonl`.
- Không sửa lịch sử; chỉ thêm event/record mới.
