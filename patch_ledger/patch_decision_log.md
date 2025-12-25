# Patch Decision Log

## 2025-12-24 — LOCK P1-THRESHOLDS (V5.0.2)

- **Decision:** Khóa `registry/thresholds.yaml` (P1-THRESHOLDS) làm SSOT cho cảnh báo & kill-switch.
- **Scope:** 20 metric kill-switch + các metric liên quan consent/evidence/SLA/cash/ops.
- **Canonical:** evidence metric = `evidence_pass_rate` (alias legacy: `risk_evidence_pass_rate`).
- **Review due:** 2026-01-07 (baseline 14 ngày).
- **Owners:** Commander (HO), Data Lead (HO), Finance Controller (HO), Field Runner (On-site).
- **Rollback:** theo patch record P1-THRESHOLDS mục 5.

## 2025-12-24 — ADD P1 Exec-Safety Pack (UnitTest + Rollback + Incident SLA)

- **Decision:** Bổ sung 3 mảnh còn thiếu để Go-live không cháy: Unit Test Spec, Rollback Procedures, Incident Response SLA.
- **SSOT:**
  - `governance/unit_test_spec.yaml` (P1-UNITTEST-SPEC)
  - `governance/rollback_procedures.yaml` (P1-ROLLBACK)
  - `governance/incident_response_sla.yaml` (P1-INCIDENT-SLA)
- **Owners:** Data Lead / Tech Lead / Commander + backup theo từng file.
- **Audit:** mọi trigger/rollback phải log append-only vào `audit/*.jsonl`.

- 2025-12-24: Added P2-INGEST skeleton (P2-INGEST_v0_1_2025-12-24.md)

## 2025-12-24 — ADD P2-TEMPLATES-MATRIX (Hard+Soft Templates v0.1)

- **Decision:** Bổ sung hệ template (hard + soft intel) để chuẩn hóa nhập liệu GĐ1 và ingest GĐ2.
- **SSOT:**
  - `registry/template_registry.yaml`
  - `registry/intel_dimensions.yaml`
  - `templates/` + `docs/templates/*`
- **Owners:** Commander, Data Lead, Field Runner, Finance Controller.
- **Notes:** Không sửa Appendix gốc; chỉ add lớp vận hành.

## 2025-12-25 — ADD P2-PLAYBOOK (Execution Playbook for Templates + Ingest)

- **Decision:** Bổ sung playbook hướng dẫn thực thi end-to-end cho GĐ1 (template → ingest → quarantine/gate/payout) để người và máy đọc hiểu thống nhất.
- **SSOT:**
  - `docs/Playbook_ThucThi_ToanTrinh_V5_0_2_GD1_YenLac_2025-12-25.docx`
- **Scope:** Tài liệu hướng dẫn (documentation only). Không thay đổi logic registry, event schema, hay thresholds.
- **Owners:** Commander (HO), Data Lead (HO), Field Runner (On-site).

