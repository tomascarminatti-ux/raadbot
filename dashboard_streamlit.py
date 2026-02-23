import streamlit as st
import json
from pathlib import Path
import time
import os

st.set_page_config(page_title="Raadbot Live", layout="wide", page_icon="🚀")
st.title("🚀 Raadbot - Visor en Vivo de GEMs")

log_file = Path("pipeline_state.json")

# Sidebar info
st.sidebar.header("Sistema")
st.sidebar.info(f"Proveedor: {os.getenv('LLM_PROVIDER', 'gemini')}")
st.sidebar.info(f"Archivo: {log_file}")

placeholder = st.empty()

while True:
    if log_file.exists():
        try:
            # Read state
            content = log_file.read_text(encoding="utf-8")
            if content:
                data = json.loads(content)
                with placeholder.container():
                    steps = data.get("steps", [])
                    # Show last steps first
                    for step in reversed(steps):
                        gem_name = step.get('gem', 'GEM')
                        status = step.get('status', 'N/A')
                        score = step.get('score', 'N/A')

                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if status == "OK":
                                st.success(f"{gem_name}")
                            elif status == "BLOCKED":
                                st.error(f"{gem_name}")
                            else:
                                st.info(f"{gem_name}")

                        with col2:
                            with st.expander(f"{step.get('action', 'Acción')} - Score: {score}"):
                                st.json(step)
        except Exception as e:
            st.error(f"Error leyendo logs: {e}")
    else:
        st.warning("Esperando a que se inicie el pipeline (archivo pipeline_state.json no encontrado)...")

    time.sleep(2)
