import segno
import streamlit as st
import io

@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "attendsense-main.streamlit.app"
    join_url = f"{app_domain}/join-code={subject_code}"  #url for joining subject
    st.subheader("SCAN TO JOIN")

    qr = segno.make(join_url)  #QR code for joining subject
    out = io.BytesIO()    #Creates an empty file-like object in RAM. This will hold the QR code image.
    qr.save(out, kind='png', scale=10, border=1)   #saving qr in png form

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### Copy link')
        st.code(join_url, language='text')
        st.code(subject_code, language='text')
        st.info("copy this link to share")

    with col2:
        st.write("### scan to join")
        st.image(out.getvalue(), caption='QR code for class joining')



