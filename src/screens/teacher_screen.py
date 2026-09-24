import streamlit as st
from src.components.footer import footer_dashboard

from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard

from src.database.db import check_teacher_credentials, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog

from src.pipelines.face_pipeline import predict_attendance

from datetime import datetime
import numpy as np
import pandas as pd

from src.database.config import supabase

from src.components.dialog_voice_attendance import voice_attendance_dialog

def teacher_screen():
    style_base_layout()
    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_login_screen()
    elif st.session_state.teacher_login_type=='register':
        teacher_registration_screen()

def teacher_dashboard():
    style_background_dashboard()
    style_base_layout()
    
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {teacher_data['name']} ")
        if st.button("Logout  ⌘ + ⌫", type='secondary', key='btn_go_home', shortcut="ctrl+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()
        
    
    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3 = st.columns(3)


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()


    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()


    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records', type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()
    
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()    
    
    
    footer_dashboard()
            
            
def teacher_tab_take_attendance():
    st.set_page_config(
            page_title="Presyra | Teacher - Take Attendance Tab",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()   
    
    
    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', width='stretch', type='tertiary', icon=':material/analytics:',disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}
                
                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)
                    
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present= len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })
                
                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
        
    with c3:
        if st.button('Use Voice Attendance',type='primary',width='stretch',icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)
    
def teacher_tab_manage_subjects():
    st.set_page_config(
            page_title="Presyra | Teacher - Manage Subjects",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
    style_base_layout()
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')
        
    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("⏰", "Classes", sub['total_classes'])
            ]
            def share_btn():
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                st.space()
            
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")
                

def teacher_tab_attendance_records():
    st.set_page_config(
            page_title="Presyra | Teacher - Attendance Records",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="collapsed",
        )

    st.header("Attendance Records")

    teacher_id = st.session_state.teacher_data["teacher_id"]

    # GET ATTENDANCE RECORDS
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found.")
        return

    # PREPARE DATA
    data = []

    for r in records:

        ts = r.get("timestamp")

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,

            "Time": (
                datetime.fromisoformat(ts).strftime(
                    "%d-%m-%Y || %I:%M %p"
                )
                if ts
                else "N/A"
            ),

            "Subject": r["subjects"]["name"],

            "Subject Code": r["subjects"]["subject_code"],

            "Student ID": r["student_id"],

            "Student Name": r["students"]["name"],

            "is_present": bool(
                r.get("is_present", False)
            )
        })

    df = pd.DataFrame(data)

    # CREATE ATTENDANCE SESSION SUMMARY
    summary = (
        df.groupby(
            [
                "ts_group",
                "Time",
                "Subject",
                "Subject Code"
            ]
        )
        .agg(
            Present_Count=("is_present", "sum"),
            Total_Count=("is_present", "count")
        )
        .reset_index()
    )

    summary["Attendance Stats"] = (
        "✅ "
        + summary["Present_Count"].astype(str)
        + " / "
        + summary["Total_Count"].astype(str)
        + " Students"
    )

    # ATTENDANCE SESSION TABLE
    st.subheader("Attendance Sessions")

    # Table Header
    header_cols = st.columns(
        [1.6, 2.8, 1.5, 1.8, 1.2]
    )
    with header_cols[0]:
        st.markdown(
            '<p style="font-size: 15px; font-weight: 600;">Time</p>',
            unsafe_allow_html=True
        )

    with header_cols[1]:
        st.markdown(
            '<p style="font-size: 15px; font-weight: 600;">Subject</p>',
            unsafe_allow_html=True
        )

    with header_cols[2]:
        st.markdown(
            '<p style="font-size: 15px; font-weight: 600;">Subject Code</p>',
            unsafe_allow_html=True
        )

    with header_cols[3]:
        st.markdown(
            '<p style="font-size: 15px; font-weight: 600;">Attendance Stats</p>',
            unsafe_allow_html=True
        )

    with header_cols[4]:
        st.markdown(
            '<p style="font-size: 15px; font-weight: 600;">Action</p>',
            unsafe_allow_html=True
        )

    # DISPLAY EACH ATTENDANCE SESSION
    for _, row in summary.sort_values(
        by="ts_group",
        ascending=False
    ).iterrows():

        cols = st.columns(
            [1.6, 2.8, 1.5, 1.8, 1.2]
        )

        with cols[0]:
            st.write(row["Time"])

        with cols[1]:
            st.write(row["Subject"])

        with cols[2]:
            st.write(row["Subject Code"])

        with cols[3]:
            st.write(row["Attendance Stats"])

        with cols[4]:

            if st.button(
                "View",
                key=(
                    f"view_attendance_"
                    f"{row['ts_group']}_"
                    f"{row['Subject Code']}"
                ),
                width="stretch"
            ):

                st.session_state["selected_attendance"] = {
                    "ts_group": row["ts_group"],
                    "time": row["Time"],
                    "subject": row["Subject"],
                    "subject_code": row["Subject Code"]
                }

                st.rerun()

        st.markdown(
            """
            <div style="
                height: 12px;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: 50%;
                    left: 0;
                    right: 0;
                    border-top: 1px solid rgba(100, 116, 139, 0.20);
                "></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # SHOW SELECTED ATTENDANCE DETAILS
    if "selected_attendance" not in st.session_state:
        return

    selected = st.session_state["selected_attendance"]

    st.subheader("Attendance Details")

    st.write(
        f"**{selected['subject']}** "
        f"• {selected['subject_code']} "
        f"• {selected['time']}"
    )

    # GET STUDENTS FOR SELECTED SESSION
    details = df[
        (df["ts_group"] == selected["ts_group"]) &
        (df["Subject Code"] == selected["subject_code"])
    ].copy()

    # CALCULATE ATTENDANCE COUNTS
    present_count = int(
        details["is_present"].sum()
    )

    total_count = len(details)

    absent_count = (
        total_count - present_count
    )

    # ATTENDANCE METRICS
    stat1, stat2, stat3 = st.columns(3)

    with stat1:
        st.metric(
            "Total Students",
            total_count
        )

    with stat2:
        st.metric(
            "Present",
            present_count
        )

    with stat3:
        st.metric(
            "Absent",
            absent_count
        )


    # STUDENT ATTENDANCE STATUS
    details["Status"] = details[
        "is_present"
    ].map({
        True: "✅ Present",
        False: "❌ Absent"
    })

    student_display = details[
        [
            "Student ID",
            "Student Name",
            "Status"
        ]
    ].copy()
    
    st.dataframe(
        student_display,
        width="stretch",
        column_config={
            "Student ID": st.column_config.TextColumn(
                "Student ID",
                width="small"
            ),
            "Student Name": st.column_config.TextColumn(
                "Student Name",
                width="large"
            ),
            "Status": st.column_config.TextColumn(
                "Status",
                width="medium"
            ),
        },
        hide_index=True
    )
    
    # CLOSE DETAILS
    if st.button(
        "Close Details",
        key="close_attendance_details"
    ):
        del st.session_state["selected_attendance"]
        st.rerun()
    st.space()
    st.space()
    st.divider()

def login_teacher(username, password):
    if not username or not password:
        return False
    
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    
    return False

def teacher_login_screen():
    st.set_page_config(
        page_title="Presyra | Teacher Login",
        page_icon="🎓",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Baloo+2:wght@600;700;800&display=swap');

        .stApp {
            background: linear-gradient(180deg, #e9e6fb 0%, #ded9fa 100%);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .block-container {
            max-width: 720px;
            padding-top: 2.5rem;
        }

        /* Top bar alignment container */
        .logo-wrap {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .logo-badge {
            width: 56px;
            height: 56px;
            background: #ffd400;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .logo-text {
            font-family: 'Baloo 2', sans-serif;
            font-weight: 800;
            font-size: 2rem;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1;
            color: #2f2bad;
            letter-spacing: -0.5px;
        }

        /* Centered Page Title */
        .page-title {
            font-family: 'Baloo 2', sans-serif;
            font-weight: 800;
            font-size: 2.3rem;
            color: #14122b;
            text-align: center;
            margin-top: 1rem;
            margin-bottom: 2.5rem;
            letter-spacing: -0.5px;
        }
        /* Field labels */
            .field-label {
                font-size: 0.85rem;
                font-weight: 600;
                color: #3d3a5c;
                margin-bottom: 0.35rem;
                margin-top: 1.1rem;
            }
        
        button[data-testid="baseButton-primary"] {
            background-color: #2563EB !important;
        }

        div[data-testid="stTextInput"] input {
            background: rgba(255,255,255,0.6) !important;
            border: 1px solid rgba(107, 99, 199, 0.15) !important;
            border-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.95rem !important;
            color: #2b2850 !important;
        }

        /* Hide the built-in keyboard shortcut text badge */
        div[data-testid="stButton"] button kbd {
            display: none !important;
        }

        /* LOGIN BUTTON — BLUE */
        div[data-testid="stButton"] button[kind="primary"] {
            background: #2563EB !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
        }

        /* LOGIN BUTTON — BLUE HOVER */
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background: #1D4ED8 !important;
            color: white !important;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.5) !important;
        }

        /* REGISTER + HOME BUTTONS — PINK */
        div[data-testid="stButton"] button[kind="secondary"] {
            background: linear-gradient(135deg, #ec4899 0%, #db2777 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            box-shadow: 0 4px 12px rgba(219, 39, 119, 0.35) !important;
        }

        /* REGISTER + HOME BUTTONS — PINK HOVER */
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #db2777 0%, #be185d 100%) !important;
            color: white !important;
            box-shadow: 0 6px 16px rgba(219, 39, 119, 0.5) !important;
        }
        
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Top bar with vertical centering applied to columns ---
    top_left, top_right = st.columns([3, 1.3], vertical_alignment="center")
    
    with top_left:
        st.markdown(
            """
            <div class="logo-wrap">
                <div class="logo-badge">🎓</div>
                <h1 class="logo-text">Presyra</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_right:
        if st.button("Go back to Home  ⌘ + ⌫", key="btn_go_home", shortcut="ctrl+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    
    # Centered Title
    st.markdown('<div class="page-title">Login to your teacher profile</div>', unsafe_allow_html=True)
    
    
    st.markdown('<div class="field-label">Enter username</div>', unsafe_allow_html=True)
    teacher_username = st.text_input("Enter Username", placeholder="@tejasgupta",label_visibility="collapsed",)
    
    st.markdown('<div class="field-label">Enter Password</div>', unsafe_allow_html=True)
    teacher_password = st.text_input("Your Password", type="password",placeholder="Enter password",label_visibility="collapsed",)
    
    st.divider()
    
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Login  ⌘ + ↵", key="btn_login", type="primary", use_container_width=True):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()           
            else:
                st.error("Invalid username or password. Please try again.")
    with btnc2:
        if st.button("Register instead",key="btn_register_instead", icon="📝",  type="secondary", width="stretch", use_container_width=True):
            st.session_state.teacher_login_type = "register"
            st.rerun()
    
    footer_dashboard()

def register_teacher(username, name, password, confirm_password):
    if not username or not name or not password:
        return False, "All fields are required."
    if check_teacher_credentials(username):
        return False, "Username already exists."
    if password != confirm_password:
        return False, "Passwords doesn't match."
    try:
        create_teacher(username, password, name)
        return True, "Teacher registered successfully! Login Now."
    except Exception as e:
        return False, "Unexpected Error!"

def teacher_registration_screen():
    st.set_page_config(
        page_title="Presyra | Teacher Registration",
        page_icon="🎓",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Baloo+2:wght@600;700;800&display=swap');

        .stApp {
            background: linear-gradient(180deg, #e9e6fb 0%, #ded9fa 100%);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .block-container {
            max-width: 720px;
            padding-top: 2.5rem;
        }

        /* Top bar */
        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
        }

        .logo-wrap {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .logo-badge {
            width: 56px;
            height: 56px;
            background: #ffd400;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .logo-text {
            font-family: 'Baloo 2', sans-serif;
            font-weight: 800;
            font-size: 1.5rem;
            line-height: 1.05;
            color: #2f2bad;
            letter-spacing: -0.5px;
        }

        /* Centered Page Title */
        .page-title {
            font-family: 'Baloo 2', sans-serif;
            font-weight: 800;
            font-size: 2.3rem;
            color: #14122b;
            text-align: center;
            margin-top: 1rem;
            margin-bottom: 2.5rem;
            letter-spacing: -0.5px;
        }

        /* Field labels */
        .field-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #3d3a5c;
            margin-bottom: 0.35rem;
            margin-top: 1.1rem;
        }

        div[data-testid="stTextInput"] input {
            background: rgba(255,255,255,0.6) !important;
            border: 1px solid rgba(107, 99, 199, 0.15) !important;
            border-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.95rem !important;
            color: #2b2850 !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #9a94c4 !important;
        }

        div[data-testid="stTextInput"] > div {
            border: none !important;
            background: transparent !important;
        }

        hr {
            border: none;
            border-top: 1px solid rgba(107, 99, 199, 0.2);
            margin: 2rem 0 1.5rem 0;
        }
        /* Hide the built-in keyboard shortcut text badge inside Streamlit buttons */
        div[data-testid="stButton"] button kbd {
            display: none !important;
        }

        /* Primary (Blue) button styling */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 0.65rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35) !important;
            width: 100% !important;
            min-height: 42px !important;
        }

        /* Secondary (Pink) button styling */
        div[data-testid="stButton"] > button[kind="secondary"] {
            background: linear-gradient(135deg, #ec4899 0%, #db2777 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 0.65rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            box-shadow: 0 4px 12px rgba(219, 39, 119, 0.35) !important;
            width: 100% !important;
            min-height: 42px !important;
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
            box-shadow: 0 6px 16px rgba(79, 70, 229, 0.5) !important;
        }

        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #db2777 0%, #be185d 100%) !important;
            box-shadow: 0 6px 16px rgba(219, 39, 119, 0.5) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Top bar ---
    top_left, top_right = st.columns([3, 1.3])
    with top_left:
        st.markdown(
            """
            <div class="logo-wrap">
                <div class="logo-badge">🎓</div>
                <div class="logo-text"><h1>Presyra</h1></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_right:
        st.markdown('<div class="pink-btn">', unsafe_allow_html=True)
        if st.button("Go back to Home  ⌘ + ⌫", key="btn_go_home", shortcut="ctrl+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Centered Title
    st.markdown('<div class="page-title">Register your teacher profile</div>', unsafe_allow_html=True)

    # --- Form fields ---
    st.markdown('<div class="field-label">Enter username</div>', unsafe_allow_html=True)
    username = st.text_input("username", placeholder="@abhishek", label_visibility="collapsed")

    st.markdown('<div class="field-label">Enter name</div>', unsafe_allow_html=True)
    name = st.text_input("name", placeholder="Full name", label_visibility="collapsed")

    st.markdown('<div class="field-label">Enter password</div>', unsafe_allow_html=True)
    password = st.text_input(
        "password",
        placeholder="Enter your password",
        type="password",
        label_visibility="collapsed",
    )

    st.markdown('<div class="field-label">Confirm password</div>', unsafe_allow_html=True)
    confirm_password = st.text_input(
        "confirm_password",
        placeholder="Confirm your password",
        type="password",
        label_visibility="collapsed",
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("👤 Register Now  ⌘ + ↵", key="btn_register", type="primary", use_container_width=True):
            success, message = register_teacher(username, name, password, confirm_password)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
    with btn_col2:
        if st.button("👤 Login instead", key="btn_login_instead", type="secondary", use_container_width=True):
            st.session_state.teacher_login_type = "login"
            st.rerun()
    
    footer_dashboard()
