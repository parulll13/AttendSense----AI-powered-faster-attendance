import streamlit as st

from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home
def home_screen():

    header_home()
    style_background_home()
    style_base_layout()
    col1, col2 = st.columns(2, gap = "large")

    with col1:
        st.header("I'm teacher")
        st.image("https://i.pinimg.com/736x/11/f9/b5/11f9b55a05f2820b6359fbe9b638b081.jpg", width = 150)
        if st.button("Teacher portal", type = "primary"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    with col2:
        st.header("I'm student")
        st.image("https://i.pinimg.com/1200x/f1/68/76/f1687663184804a0ddd02d608811316d.jpg", width = 150)
        if st.button("Student Portal", type="primary"):
            st.session_state['login_type'] = 'student'
            st.rerun()

    footer_home()