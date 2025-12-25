# Incident Response SLA (P1-INCIDENT-SLA)

SSOT: `governance/incident_response_sla.yaml`

## Mục tiêu
- Không để Tier 3 kéo dài vì “không ai nghe máy”.

## SLA theo tier
- Tier 1 Warning: phản hồi 15 phút, xử lý 1h.
- Tier 2 Throttle: phản hồi 5 phút, xử lý 30 phút.
- Tier 3 Hard Stop: phản hồi 2 phút, xử lý 15 phút.

## Escalation
- Tier 2 >2h chưa resolve → CEO.
- Tier 3 >1h chưa mở lại → HĐQT.
