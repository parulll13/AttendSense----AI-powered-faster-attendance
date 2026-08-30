import streamlit as st

from src.ui.base_layout import style_base_layout, style_background_dashboard
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    st.title("Teacher Screen")