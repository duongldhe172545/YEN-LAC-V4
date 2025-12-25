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
# - preflight: tiền kiểm (kiểm tra trước khi nạp)
# - lint: soi lỗi định dạng (kiểm tra quy ước)
# - schema: khuôn dữ liệu (định nghĩa cột/kiểu)

st.set_page_config(page_title="Preflight Runner", layout="wide")
st.title("Preflight Runner")

regs = load_registries()
repo_root = Path(regs["repo_root"]).resolve()

schema_dir = repo_root / "templates" / "schema_generated"
if not schema_dir.exists():
    st.error(f"Thiếu templates/schema_generated: {schema_dir}")
    st.stop()

schema_files = sorted(schema_dir.glob("*.schema.yaml"))

def template_code_from_schema(p: Path) -> str:
    # A7_events_evt_star.schema.yaml -> A7_events_evt_star
    name = p.name
    if name.endswith(".schema.yaml"):
        return name[: -len(".schema.yaml")]
    return name

template_codes = [template_code_from_schema(p) for p in schema_files]

col1, col2 = st.columns([1, 1])
with col1:
    template_code = st.selectbox("template_code (từ templates/schema_generated)", template_codes)

with col2:
    st.write("Gợi ý: demo_inputs/hard/*_demo.csv, demo_inputs/events/events_demo.csv")

uploaded = st.file_uploader("Upload CSV hoặc Excel (XLSX)", type=["csv", "xlsx"])

# append-only run log
run_log = repo_root / "data" / "audit" / "preflight_run_log.jsonl"

if uploaded is not None:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    up_dir = repo_root / "data" / "uploads" / "preflight"
    up_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".csv" if uploaded.name.lower().endswith(".csv") else ".xlsx"
    saved_path = up_dir / f"{ts}__{uploaded.name.replace(' ', '_')}"
    # write bytes
    saved_path.write_bytes(uploaded.getbuffer())
    st.success(f"Đã lưu upload (append-only): {saved_path}")

    # Convert XLSX -> CSV temp if needed
    input_path = saved_path
    if suffix == ".xlsx":
        try:
            df = pd.read_excel(saved_path)
        except Exception as e:
            st.error("Đọc XLSX thất bại. Nếu máy mày chưa có openpyxl, cài: pip install openpyxl")
            st.exception(e)
            st.stop()
        csv_path = saved_path.with_suffix(".csv")
        df.to_csv(csv_path, index=False, encoding="utf-8")
        input_path = csv_path
        st.info(f"Đã convert XLSX -> CSV: {input_path}")

    # Call preflight script (subprocess) for consistent behavior
    script = repo_root / "code" / "scripts" / "preflight_templates.py"
    if not script.exists():
        st.error(
            "Thiếu code/scripts/preflight_templates.py. Nếu mày chưa merge addon, copy file này vào đúng chỗ."
        )
        st.stop()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "code") + (os.pathsep + env.get("PYTHONPATH", ""))

    if st.button("RUN PREFLIGHT (lint)", type="primary"):
        cmd = [
            sys.executable,
            str(script),
            "--repo_root",
            str(repo_root),
            "--template_code",
            template_code,
            "--input_csv",
            str(input_path),
        ]
        started = time.time()
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        took = time.time() - started

        append_jsonl(
            run_log,
            {
                "ts_epoch": int(time.time()),
                "template_code": template_code,
                "input_path": str(input_path),
                "returncode": res.returncode,
                "seconds": round(took, 3),
            },
        )

        st.subheader("Result")
        if res.returncode == 0:
            st.success("PASS")
        else:
            st.error("FAIL")
        st.code((res.stdout or "") + "\n" + (res.stderr or ""))

st.divider()
st.subheader("Recent preflight runs (append-only log)")
rows = read_jsonl(run_log)
if rows:
    st.dataframe(pd.DataFrame(rows).tail(200), use_container_width=True)
else:
    st.info("Chưa có run.")
