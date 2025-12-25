# P1-INCIDENT-SLA (V5.0.2) — 2025-12-24

## Mục tiêu
Khóa SLA phản ứng cho kill-switch tier để không cháy vì “trễ tay”.

## SSOT
- `governance/incident_response_sla.yaml`
- (doc) `docs/governance/Incident_Response_SLA.md`

## Overlay vào Hiến Pháp (gợi ý vị trí)
- Section 11.4.2: Incident Response SLA

## PASS/FAIL
PASS khi:
- Tier 1/2/3 có response_time + action_time
- Có backup_owner + escalation
