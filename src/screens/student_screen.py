import streamlit as st
import time
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.ui.base_layout import style_base_layout, style_background_dashboard

from PIL import Image
import numpy as np

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)

from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_attendance, get_student_subject, unenroll_student_to_subject
from src.components.subject_card import subject_card

def student_dashboard():
    st.set_page_config(
            page_title="Presyra | Student Dashboard",
            page_icon="🎓",
            layout="centered",
            initial_sidebar_state="collapsed",
        )
    style_background_dashboard()
    style_base_layout()
    
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']} ")
        if st.button("Logout  ⌘ + ⌫", type='secondary', key='btn_go_home', shortcut="ctrl+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()
            
    st.space()
    
    c1, c2 = st.columns(2, vertical_alignment='bottom')
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subject(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']
        
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        
        stats_map[sid]['total'] += 1
        
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        
        stats = stats_map.get(sid, {"total": 0, "attended": 0})
        
        def unenroll_button(sub, student_id):
            if st.button("Unenroll from this course", type="tertiary", width="stretch", icon=":material/delete_forever:", key=f"unenroll_{sub['subject_id']}"):
                unenroll_student_to_subject(student_id, sub['subject_id'])
                st.toast(f"Unenrolled from {sub['name']} successfully!")
                st.rerun()
                
        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('🗓️', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=lambda: unenroll_button(sub, student_id)
            )
            
    footer_dashboard()

    
def student_screen():

    st.set_page_config(
        page_title="Presyra | Student- Login/Registration ",
        page_icon="🎓",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    style_background_dashboard()
    style_base_layout()
    
    # If student is already logged in
    if "student_data" in st.session_state:
        student_dashboard()
        return

    # Initialize registration state
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    if "registration_photo" not in st.session_state:
        st.session_state.registration_photo = None

    # Header
    c1, c2 = st.columns(
        2,
        vertical_alignment="bottom",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home  ⌘ + ⌫",
            type="secondary",
            key="loginbackbtn",
            shortcut="ctrl+backspace"
        ):
            st.session_state["login_type"] = None
            st.session_state.show_registration = False
            st.session_state.registration_photo = None
            st.rerun()

    # Login 
    st.header(
        "Login using FaceID",
        text_alignment="center"
    )

    st.space()
    st.space()

    # Camera
    photo_source = st.camera_input(
        "Position your face in the center"
    )

    # Process captured face
    if photo_source:

        # Save captured photo in session state.
        # This is important because Streamlit reruns the app
        # when text_input/audio_input changes.
        st.session_state.registration_photo = photo_source

        img = np.array(
            Image.open(photo_source)
        )

        with st.spinner("AI is Scanning..."):

            detected, all_ids, num_faces = predict_attendance(img)

        # No face detected
        if num_faces == 0:

            st.warning(
                "Face not found! Please position your face "
                "properly in the camera."
            )

            st.session_state.show_registration = False
            
        # Multiple faces detected
        elif num_faces > 1:

            st.warning(
                "Multiple faces found! "
                "Please make sure only one person is visible."
            )

            st.session_state.show_registration = False
            
        # Exactly one face detected
        else:
            # Recognized student
            if detected:

                student_id = list(
                    detected.keys()
                )[0]

                all_students = get_all_students()

                student = next(
                    (
                        s
                        for s in all_students
                        if s["student_id"] == student_id
                    ),
                    None
                )

                if student:

                    # Student successfully recognized
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.student_data = student

                    # Clear registration state
                    st.session_state.show_registration = False
                    st.session_state.registration_photo = None

                    st.toast(
                        f"Welcome Back {student['name']}"
                    )

                    time.sleep(1)
                    st.rerun()

            # Unknown student
            else:

                st.info(
                    "Face not recognized! "
                    "You might be a new student."
                )

                # Keep registration form visible
                st.session_state.show_registration = True

    # Registration Form
    if st.session_state.show_registration:

        with st.container(border=True):

            st.header("Register New Profile")

            # Make sure we have a captured photo
            if st.session_state.registration_photo is None:

                st.warning(
                    "Please capture your face using the camera "
                    "before registration."
                )

            else:

                new_name = st.text_input(
                    "Enter your name",
                    placeholder="E.g. MD Kaif",
                    key="new_student_name"
                )
                
                # Voice Enrollment
                st.subheader("Optional: Voice Enrollment")

                st.info(
                    "Enroll your voice for voice-only attendance."
                )

                audio_data = None

                try:

                    audio_data = st.audio_input(
                        "Record a short phrase like: "
                        "I am present, my name is Kaif."
                    )

                except Exception:

                    st.error(
                        "Audio data failed."
                    )

                # Create Account
                if st.button(
                    "Create Account",
                    type="primary",
                    key="create_student_account"
                ):

                    if not new_name.strip():

                        st.warning(
                            "Please enter your name!"
                        )

                    else:

                        with st.spinner(
                            "Creating profile..."
                        ):

                            # Get saved camera photo
                            photo = (
                                st.session_state.registration_photo
                            )

                            img = np.array(
                                Image.open(photo)
                            )

                            # Extract face embedding
                            encoding = get_face_embeddings(
                                img
                            )
                            
                            # Face embedding failed
                            if not encoding:

                                st.error(
                                    "Couldn't capture your facial "
                                    "features for registration."
                                )
                                
                            # More than one face during registration
                            elif len(encoding) > 1:

                                st.error(
                                    "Multiple faces detected. "
                                    "Please register with only your face "
                                    "visible."
                                )

                            # Successfully captured face
                            else:

                                face_emb = encoding[0].tolist()
                                
                                # Optional voice embedding
                                voice_emb = None

                                if audio_data:

                                    try:

                                        voice_emb = (
                                            get_voice_embedding(
                                                audio_data.read()
                                            )
                                        )

                                    except Exception:

                                        st.warning(
                                            "Voice enrollment failed, "
                                            "but your face profile can "
                                            "still be created."
                                        )

                                        voice_emb = None

                                # Save student in database
                                response_data = create_student(
                                    new_name.strip(),
                                    face_embedding=face_emb,
                                    voice_embedding=voice_emb
                                )

                                # Account created
                                if response_data:

                                    # Clear cached face classifier
                                    train_classifier()

                                    # Login student
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = "student"
                                    st.session_state.student_data = (
                                        response_data[0]
                                    )

                                    # Clear registration state
                                    st.session_state.show_registration = False
                                    st.session_state.registration_photo = None

                                    st.toast(
                                        f"Profile created! "
                                        f"Hi {new_name.strip()}"
                                    )

                                    time.sleep(1)
                                    st.rerun()

                                else:

                                    st.error(
                                        "Failed to create student profile."
                                    )

    # Footer
    footer_dashboard()