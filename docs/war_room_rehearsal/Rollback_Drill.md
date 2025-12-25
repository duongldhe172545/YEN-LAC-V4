# Rollback Drill — registry + code + data

## 1) Registry rollback (<= 2h)
**Khi nào:** alias collision, thresholds sai tier, fatal linter.

**Steps:**
1. Xác định commit/patch gây lỗi (patch_ledger + decision log).
2. Git revert commit hash.
3. Chạy `python code/scripts/validate_registry.py --repo_root .` PASS.
4. Reload registry trong app (restart Streamlit).
5. Log AAR: thời gian + người thực thi + ảnh hưởng.

## 2) Code rollback (<= 30 phút)
**Khi nào:** bug payout/fraud detection.

**Steps:**
1. Rollback Docker image về tag trước.
2. Smoke test 3 trang: Registry Viewer, Quarantine Queue, Kill Switch Panel.
3. Xác nhận kill-switch còn hoạt động.

## 3) Data ingest rollback (tùy mức)
**Nguyên tắc:** event append-only, rollback bằng **quarantine + compensate event** chứ không xóa lịch sử.
