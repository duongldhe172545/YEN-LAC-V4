# Registry Contract (máy đọc)

## events.yaml
- event_code: EVT_[A-Z0-9_]+
- required_fields: list
- evidence_required: bool
- idempotency_key_fields: list

## metrics.csv
Bắt buộc các cột tối thiểu:
- metric_code, k_level, unit, grain, window, owner, source

## metric_alias.yaml
- canonical -> [aliases]
- Không được alias 2 canonical trùng nhau

## gate_matrix.yaml
- gate_code, required_events, required_metrics, block_payout (bool), quarantine_reason

## registry_lints.yaml
- rules: regex + severity(FATAL/WARN) + target(file/field)
