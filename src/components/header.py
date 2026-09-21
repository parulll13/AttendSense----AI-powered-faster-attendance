import streamlit as st
import base64
from pathlib import Path

def header_home():

    project_root = Path(__file__).resolve().parents[2]
    assets_folder = project_root / "assets"
    logo = assets_folder / "attendsense.png"

    st.write("PROJECT ROOT:", project_root)
    st.write("ASSETS EXISTS:", assets_folder.exists())
    st.write("ASSETS FILES:", list(assets_folder.iterdir()) if assets_folder.exists() else "NO ASSETS FOLDER")
    st.write("LOGO PATH:", logo)
    st.write("LOGO EXISTS:", logo.exists())

    
    # logo = Path(__file__).resolve().parents[2] / "assets" / "attendsense.png"
    with open(logo, "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style = "display: flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:10px; margin-top:30px">
        <img src="data:image/png;base64,{logo}" style = "height:200px"/>
    </div>
            """,unsafe_allow_html = True
    )


def header_dashboard():

    project_root = Path(__file__).resolve().parents[2]
    logo = project_root / "assets" / "attendsense.png"

    # logo = Path(__file__).resolve().parents[2] / "assets" / "attendsense.png"

    with open(logo, "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style = "display: flex; align-items:center; justify-content:center; gap: 10px">
        <img src="data:image/png;base64,{logo}" style = "height:100px"/>
    </div>
            """,unsafe_allow_html = True
    )