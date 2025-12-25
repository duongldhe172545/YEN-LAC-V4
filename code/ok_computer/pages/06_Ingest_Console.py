import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from audit_store import append_jsonl, read_jsonl
from registry_loader import load_registries

# English → Việt:
# - ingest: nạp (đưa dữ liệu vào hệ thống)
# - event store: kho sự kiện (nơi lưu nhật ký event)
# - quarantine: cách ly (bản ghi lỗi không vào event store)
# - KPI (Key Performance Indicator): chỉ số đo hiệu suất

st.set_page_config(page_title="Ingest Console", layout="wide")
st.title("Ingest Console")

regs = load_registries()
repo_root = Path(regs["repo_root"]).resolve()

# Paths (append-only outputs)
event_log_path = repo_root / "data" / "event_store" / "event_log.jsonl"
quarantine_path = repo_root / "data" / "quarantine" / "quarantine_events.jsonl"
audit_path = repo_root / "data" / "audit" / "ingest_audit.jsonl"

st.caption(f"event_log: {event_log_path}")

col1, col2 = st.columns([1, 1])
with col1:
    uploaded = st.file_uploader("Upload events CSV", type=["csv"], help="Theo docs/ingest_contract.md")
with col2:
    source_batch_id = st.text_input(
        "source_batch_id (mã batch nguồn)",
        value=f"BATCH_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        help="Ví dụ: VDCD_20251224_001",
    )

run_log = repo_root / "data" / "audit" / "ingest_run_log.jsonl"

if uploaded is not None:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    up_dir = repo_root / "data" / "uploads" / "ingest"
    up_dir.mkdir(parents=True, exist_ok=True)
    saved_path = up_dir / f"{ts}__{uploaded.name.replace(' ', '_')}"
    saved_path.write_bytes(uploaded.getbuffer())
    st.success(f"Đã lưu upload (append-only): {saved_path}")

    script = repo_root / "code" / "scripts" / "ingest_events.py"
    if not script.exists():
        st.error("Thiếu code/scripts/ingest_events.py")
        st.stop()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "code") + (os.pathsep + env.get("PYTHONPATH", ""))

    if st.button("RUN INGEST", type="primary"):
        cmd = [
            sys.executable,
            str(script),
            "--repo_root",
            str(repo_root),
            "--input_csv",
            str(saved_path),
            "--source_batch_id",
            source_batch_id,
        ]
        started = time.time()
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        took = time.time() - started

        append_jsonl(
            run_log,
            {
                "ts_epoch": int(time.time()),
                "input_path": str(saved_path),
                "source_batch_id": source_batch_id,
                "returncode": res.returncode,
                "seconds": round(took, 3),
            },
        )

        st.subheader("Result")
        if res.returncode == 0:
            st.success("INGEST DONE")
        else:
            st.error("INGEST FAILED")
        st.code((res.stdout or "") + "\n" + (res.stderr or ""))

st.divider()

# Snapshot counts

def count_lines(p: Path) -> int:
    if not p.exists():
        return 0
    with p.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("event_count", count_lines(event_log_path))
with c2:
    st.metric("quarantine_count", count_lines(quarantine_path))
with c3:
    st.metric("ingest_audit_records", count_lines(audit_path))

st.subheader("Latest ingest audit")
audits = read_jsonl(audit_path)
if audits:
    st.json(audits[-1])
else:
    st.info("Chưa có ingest audit.")

st.subheader("Recent ingest runs (append-only log)")
runs = read_jsonl(run_log)
if runs:
    st.dataframe(pd.DataFrame(runs).tail(200), use_container_width=True)
else:
    st.info("Chưa có run.")

st.divider()

# KPI pulse convenience
st.subheader("KPI Pulse (demo)")
st.caption("Chạy script demo_kpi_pulse.py để tạo snapshot KPI từ event_store (không thay SSOT).")
script_kpi = repo_root / "code" / "scripts" / "demo_kpi_pulse.py"
if not script_kpi.exists():
    st.warning("Thiếu code/scripts/demo_kpi_pulse.py (merge addon vào code/scripts/)")
else:
    if st.button("RUN KPI PULSE"):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root / "code") + (os.pathsep + env.get("PYTHONPATH", ""))
        cmd = [sys.executable, str(script_kpi), "--repo_root", str(repo_root)]
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if res.returncode == 0:
            st.success("KPI pulse generated")
        else:
            st.error("KPI pulse failed")
        st.code((res.stdout or "") + "\n" + (res.stderr or ""))
