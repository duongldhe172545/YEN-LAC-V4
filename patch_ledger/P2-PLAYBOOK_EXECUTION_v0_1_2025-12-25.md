# P2-PLAYBOOK_EXECUTION v0.1 (2025-12-25)

## 1. Mục tiêu
Bổ sung 01 playbook hướng dẫn thực thi toàn trình cho GĐ1: từ template (hard + soft) → ingest → quarantine/gate/payout, theo đúng nguyên tắc LOCKED (registry-first, append-only, EVT_* + idempotency_key, provider-neutral, consent/PII kill-switch, evidence-gate).

## 2. Thay đổi
- ADD: `docs/Playbook_ThucThi_ToanTrinh_V5_0_2_GD1_YenLac_2025-12-25.docx`

## 3. Không thay đổi
- Không sửa registry/events.yaml, registry/template_registry.yaml, registry/thresholds.yaml.
- Không sửa Appendix gốc.

## 4. Kiểm tra tối thiểu (manual)
- Mở doc và kiểm: có mục Data contract, Template matrix, Golden Path EVT_*, Quarantine/Gate/Kill-switch, ML-ready cho dữ liệu mềm.
- Đảm bảo các thuật ngữ tiếng Anh có giải nghĩa tiếng Việt.

## 5. Rollback
- Nếu cần rollback: xóa file doc trong `docs/` và xóa entry tương ứng trong patch_decision_log (append-only: thêm entry rollback).

