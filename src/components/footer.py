import streamlit as st

def footer_home():

    st.markdown(f"""
    <div style = "display: flex; gap: 6px; align-items:center; justify-content:center; margin-top:10px">
        <p style = " font-weight: bold; color: silver">created by Parul Gupta</p>
    </div>
            """,unsafe_allow_html = True
    )