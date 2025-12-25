# MERGELOG - P1 (A8 Runbook Hardening) into Hiến Pháp V5.0.2
Date: 2025-12-24

## 1) Overlay mới (đặt trong Appendix A8)
- `Appendix_A8_OKC_Runbook_Canonical_Aligned_V5.0.2_2025-12-24.docx`
- `Appendix_A8_OKC_Runbook_Canonical_Aligned_V5.0.2_2025-12-24.md`

Nguyên tắc: giữ nguyên A8 gốc (bằng chứng), overlay này là bản canonical cho vận hành/code.

## 2) Registry/YAML mới (đặt trong /registry hoặc /governance)
- `runbook_actions_V5.0.2_2025-12-24.yaml`
- `registry_lints_V5.0.2_2025-12-24.yaml`

## 3) Liên kết bắt buộc (để đồng bộ toàn trình)
A8 overlay assume các file SSOT sau đã có trong /registry:
- `registry_event_taxonomy_yenlac_v1_7_2025-12-24.yaml` (A3/P0.2)
- `registry_metrics_v5_0_2_extended_with_K7_2025-12-24.csv` (A4/P0.3)
- `registry_metric_alias_v5_0_2_2025-12-24.yaml` (PA2)
- `registry_gate_matrix_v1_0_2025-12-24.yaml` (A7/P1)
- `registry_causal_edges_k0_k8_yenlac_v1_2_2025-12-24.yaml` (A1/P1)

## 4) Việc phải làm sau khi merge (Go-live checklist)
1) Run registry lints (FATAL phải = 0)
2) Run unit tests (coverage >= 90%)
3) Smoke test: ingest events + compute 5 metrics lõi
4) Tabletop drill: Tier 2 + Tier 3 (kill-switch) + rollback registry
