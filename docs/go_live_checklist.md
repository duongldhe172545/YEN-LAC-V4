# Go-live Checklist (GATE-0 READY-TO-LAUNCH)

## 1) Registry & SSOT
- [ ] events.yaml lint PASS (EVT_* + required_fields + idempotency)
- [ ] metrics.csv lint PASS (unit/grain/window/owner)
- [ ] metric_alias.yaml PASS (no collision)
- [ ] gate_matrix.yaml PASS (No Evidence + Bad Evidence No Pay)
- [ ] registry_lints.yaml enabled in CI

## 2) Data & Consent
- [ ] Pending_Consent_Aging policy active (>48h cảnh báo/ép xin consent hoặc xóa)
- [ ] Không lưu PII khi chưa consent (kill-switch rule)
- [ ] Evidence pack hashing/uri index chạy được

## 3) Ops & Cash
- [ ] Payout pipeline có chặn theo Gate
- [ ] DSO metric available + threshold tiers
- [ ] Rollback drills PASS (registry/code/data)

## 4) Incident Response
- [ ] Tier-1/2/3 owners + backup owners xác nhận
- [ ] Escalation path lên CEO/HĐQT rõ

\n## Added in V5.0.2: Thresholds + CI + rehearsal\n- Thresholds registry locked: registry/thresholds.yaml (P1-THRESHOLDS).\n- CI workflow: .github/workflows/ci.yml (registry lint + pytest).\n- Rehearsal kit: docs/war_room_rehearsal/.\nEOF

echo 'Repo updated.'
