import streamlit as st
import numpy as np
from PIL import Image
import time
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Logout", type='secondary', key='logoutbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1 , c2 = st.columns(2)
    with c1:
        st.subheader("Your Enrolled Subjetcts")
    with c2:
        if st.button("Enroll in subject", type='primary', width='stretch'):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading your all subjects..."):
        subjects = get_student_subjects(student_id)  # Get all subjects in which this student is enrolled
        logs = get_student_attendance(student_id)    # Get all attendance records of this student  

        stats_map = {}   #It's a dictionary of dictionary which have total classes & classes attended by student
        for log in logs:
            sid = log['subject_id']
            if sid not in stats_map:
                stats_map[sid] = {'Total':0, 'Attended':0}

            stats_map[sid]['Total'] += 1

            if log.get['is_present']:
                stats_map[sid]['Attended'] += 1

        cols= st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub_node['subject_id']

            stats = stats_map.get(sid, {'Total':0, 'Attended':0})

            def unenroll_button():
                if st.button('Unenroll from this course',  type='tertiary', width='content', key=f'unenroll_{sid}'):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f"Successfully unenrolled from {sub['name']} course!")
                    st.rerun()

            with cols[i%2]:
                subject_card(
                    name=sub['name'],
                    code = sub['subject_code'],
                    section = sub['section'],
                    stats = [
                        ('📆', 'Total', stats['Total'] ),
                        ('✅', 'Attended', stats['Attended'])
                    ],
                    footer_callback = unenroll_button
                )


            





    footer_dashboard()



def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
        
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("""
        <h3 style="text-align: center; color: black;">Login with FaceID</h3>"""
            ,unsafe_allow_html = True)

    show_registration = False

    photo_source = st.camera_input("Position your face in the center")
    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner('AI is spinning..'):
            detected, all_ids, num_faces = predict_attendance(img)
            if num_faces == 0:
                st.warning("Face not found")
            elif num_faces>1:
                st.warning("Multiple faces found")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()

                    #Find the student whose ID is same as student_id and store it in student else store None
                    student = next((s for s in all_students if s["student_id"] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome back {student['name']}")
                        time.sleep(1)
                        st.rerun()

                else:
                    st.info("Face not detected! You might be a new student !")
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header("Register new profile")
            new_name = st.text_input("Enter your name")
            st.subheader("Optional: Voice enrollment")
            st.info("Enroll you for voice only attendence")

            audio_data = None

            try:
                audio_data = st.audio_input("Record a short phrase. Eg: My name is John and I am present")
            except Exception:
                st.error("Audio data failed")

            if st.button("Create account", type='primary'):
                if new_name:
                    with st.spinner("Creating your profile.."):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read()) #read used for converting audio into binary form

                            response_data = create_student(new_name, face_embedding = face_emb, voice_embedding = voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile created! Hi {new_name}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Couldn't capture your facial features for registration ")
                else:
                    st.warning("Please enter your name")
            
    st.space()
    st.space()
    footer_dashboard()