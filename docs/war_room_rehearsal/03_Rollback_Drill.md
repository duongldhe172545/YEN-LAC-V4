# Rollback drill (registry / code / data)

## 1) Registry rollback
- Điều kiện: alias collision / fatal linter / thresholds sai
- Steps:
  1. Git revert commit hash
  2. Re-load registry version trước
  3. Run: python code/scripts/validate_registry.py --repo_root .
  4. Smoke test Streamlit pages

## 2) Code rollback
- Điều kiện: bug ảnh hưởng payout/fraud detection
- Steps:
  1. Deploy previous Docker image (nếu có)
  2. Verify kill-switch operational

## 3) Data rollback (ingest)
- Điều kiện: ingest sai schema / duplicate event flood
- Steps:
  1. Stop ingest
  2. Quarantine batch_id
  3. Re-run ingest with corrected mapping
