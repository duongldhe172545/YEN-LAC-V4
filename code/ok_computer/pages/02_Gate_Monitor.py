import streamlit as st

from registry_loader import load_registries

st.set_page_config(page_title="Gate Monitor", layout="wide")
st.title("Gate Monitor")

regs = load_registries()
gate = regs["gate_matrix"] or {}

meta = gate.get("meta", {})
st.caption(f"gate_matrix version: {meta.get('version')} | build_date: {meta.get('build_date')}")

st.subheader("Gate Matrix (No Evidence No Pay)")
st.json(gate.get("gates", gate))

st.info("Lưu ý: Đây là bản hiến pháp hóa. Gate runtime sẽ đọc matrix + evidence log thực tế.")
