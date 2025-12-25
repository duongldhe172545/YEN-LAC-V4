import time
from pathlib import Path

import pandas as pd
import streamlit as st

from audit_store import append_jsonl, read_jsonl
from registry_loader import load_registries

st.set_page_config(page_title="Quarantine Queue", layout="wide")
st.title("Quarantine Queue")

regs = load_registries()
repo_root = Path(regs["repo_root"])
log_path = repo_root / "audit" / "quarantine_queue.jsonl"

st.caption(f"Log: {log_path}")

records = read_jsonl(log_path)
if records:
    df = pd.DataFrame(records)
    st.dataframe(df.sort_values(by=df.columns[0], ascending=False), use_container_width=True)
else:
    st.info("Chưa có record.")

st.divider()
st.subheader("Thêm record quarantine (append-only)")
with st.form("add_q"):
    scope = st.selectbox("Scope", ["house", "lead", "job", "transaction", "system"])
    entity_id = st.text_input("entity_id (house_id/lead_id/job_id/txn_id)")
    reason = st.text_area("reason")
    evidence_ref = st.text_input("evidence_ref (event_id / file / uri)")
    severity = st.selectbox("severity", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    submitted = st.form_submit_button("Append")

if submitted:
    rec = {
        "ts_epoch": int(time.time()),
        "scope": scope,
        "entity_id": entity_id,
        "severity": severity,
        "reason": reason,
        "evidence_ref": evidence_ref,
        "status": "OPEN",
    }
    append_jsonl(log_path, rec)
    st.success("Đã append.")
    st.rerun()
