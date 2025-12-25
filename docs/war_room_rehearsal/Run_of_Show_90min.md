# War-room rehearsal (90 phút) — V5.0.2

## Mục tiêu
- Diễn tập 3 thứ: Trigger → Quarantine → Action tier (Warning/Throttle/Hard Stop) → Rollback.
- Chỉ đo 2 KPI: **thời gian phản ứng** và **đúng vai** (owner/backup/escalation).

## Vai trò (đúng hiến pháp)
- Commander (HO) — chủ trì, quyết định tier 3
- Data Lead (HO) — registry, data, consent/PII
- Finance Controller (HO) — payout, DSO, freeze
- Ops Lead (HO/OS) — throttle/stop job
- Field Runner (On-site) — thực thi hiện trường, bằng chứng
- QA Lead — chất lượng, evidence integrity

## Timeline
1. 0-10'  Warm-up: kiểm tra repo + registry lint PASS
2. 10-35' Scenario A (Tier 2 Throttle)
3. 35-60' Scenario B (Tier 3 Hard Stop)
4. 60-80' Rollback drill (registry + code)
5. 80-90' After-action review (AAR) + quyết định patch backlog
