import subprocess
import sys
from pathlib import Path

import streamlit as st

from registry_loader import load_registries

st.set_page_config(page_title="OK Computer - Yen Lac", layout="wide")

st.title("OK Computer: D2Com Pilot Yên Lạc")
st.caption("V5.0.2 registries-first. Đây là bảng điều khiển để đọc Registry + chạy drill không cháy.")

regs = load_registries()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Registry Snapshot")
    meta = (regs.get("thresholds") or {}).get("meta", {})
    st.write({
        "thresholds.version": meta.get("version"),
        "thresholds.patch_id": meta.get("patch_id"),
        "effective_date": meta.get("effective_date"),
        "timezone": meta.get("timezone"),
    })

with col2:
    st.subheader("Quick Links")
    st.markdown("- `registry/` là SSOT cho code.\n- `docs/` là playbook cho người.\n- `patch_ledger/` là lịch sử vá (append-only).")

with col3:
    st.subheader("Registry Lint")
    if st.button("Chạy validate_registry.py"):
        repo_root = Path(regs["repo_root"]) if isinstance(regs.get("repo_root"), str) else Path(".")
        cmd = [
            sys.executable,
            str(repo_root / "code" / "scripts" / "validate_registry.py"),
            "--repo_root",
            str(repo_root),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            st.success("PASS")
        else:
            st.error("FAIL")
        st.code((res.stdout or "") + "\n" + (res.stderr or ""))

st.divider()

st.subheader("How to run")
st.code("""pip install -r requirements.txt
streamlit run code/ok_computer/app.py
""")

st.info("Pages nằm ở sidebar (Streamlit Pages).")
