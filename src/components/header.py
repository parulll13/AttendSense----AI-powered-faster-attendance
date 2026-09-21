import streamlit as st
import base64
from pathlib import Path

def header_home():
    
    logo = Path(__file__).resolve().parents[2] / "assets" / "attendsense.png"
    with open(logo, "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style = "display: flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:10px; margin-top:30px">
        <img src="data:image/png;base64,{logo}" style = "height:200px"/>
    </div>
            """,unsafe_allow_html = True
    )


def header_dashboard():

    logo = Path(__file__).resolve().parents[2] / "assets" / "attendsense.png"

    with open(logo, "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style = "display: flex; align-items:center; justify-content:center; gap: 10px">
        <img src="data:image/png;base64,{logo}" style = "height:100px"/>
    </div>
            """,unsafe_allow_html = True
    )