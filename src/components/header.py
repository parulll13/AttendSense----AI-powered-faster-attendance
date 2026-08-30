import streamlit as st
import base64

def header_home():
    logo = r"C:/Users/acer/Pictures/snapclass.jpg"

    with open(logo, "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style = "display: flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:10px; margin-top:30px">
        <img src="data:image/png;base64,{logo}" style = "height:100px"/>
        <h1 style="text-align:center; color: black">Snap Class</h1> 
    </div>
            """,unsafe_allow_html = True
    )