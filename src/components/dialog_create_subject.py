import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of your subject")
    sub_id = st.text_input("Enter subject code", placeholder='CS101')
    sub_name = st.text_input("Enter subject name", placeholder='Intro to Computer Science')
    sub_section = st.text_input("Enter section", placeholder='A')

    if st.button("Create Subject now", type='primary', width='stretch'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("subject created successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
        else:
            st.error("All fields are required")