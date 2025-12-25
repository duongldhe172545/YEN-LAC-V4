# P2-TEMPLATES-MATRIX_v0_1_2025-12-24

## 1) Mục tiêu
Bổ sung “hệ template” (hard + soft) để chuyển từ khung SSOT sang chạy thực địa:
- Registry-first, append-only, EVT_*, idempotency_key, provider-neutral
- Consent/PII: không lưu PII khi chưa consent; Unconsented_PII_Risk là kill-switch
- Gate: No Evidence + Bad Evidence No Pay

## 2) Thay đổi (append-only)
### Added
- `registry/template_registry.yaml` — đăng ký danh mục template + keys + stage
- `registry/intel_dimensions.yaml` — catalog enum/dimension cho dữ liệu mềm (intel)
- `docs/templates/template_matrix_v5_0_2.md` — ma trận template + hướng dẫn nhanh
- `docs/templates/excel_master_tabs_v0_1.md` — cấu trúc tab Excel gợi ý
- `templates/` — CSV templates (hard/soft) + ví dụ 1 dòng

## 3) Không sửa Appendix gốc
- Không chạm nội dung `06_Source_Appendix_Raw/*` (giữ audit).
- Đây là bổ sung vận hành ở lớp repo/registry/templates.

## 4) Owners
- Commander (HO)
- Data Lead (HO)
- Field Runner (On-site)
- Finance Controller (HO)

## 5) Rollback
- Xóa các file mới ở mục 2) Added và revert README section (nếu cần).
- Không ảnh hưởng các registry/thresholds đã LOCKED.
