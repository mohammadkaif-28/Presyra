import streamlit as st
from src.components.footer import footer_home



def home_screen():
    st.set_page_config(
        page_title="Presyra | Smart Attendance Suite",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        .stApp {
            background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 70%);
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #f8fafc;
        }

        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .hero-wrapper {
            text-align: center;
            padding: 3rem 1rem 2rem 1rem;
        }

        .app-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #818cf8;
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            backdrop-filter: blur(10px);
        }

        .main-title {
            font-size: 3.2rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -1px;
            margin-bottom: 0.75rem;
        }

        .main-subtitle {
            font-size: 1.1rem;
            color: #94a3b8;
            max-width: 600px;
            margin: 0 auto 2.5rem auto;
            line-height: 1.6;
        }

        /* Modern Glassmorphic Cards with bottom padding to house the button inside */
        .portal-card {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 2.5rem 2rem 5rem 2rem;
            backdrop-filter: blur(16px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            text-align: center;
            position: relative;
        }

        .portal-card:hover {
            transform: translateY(-8px);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 30px 60px rgba(99, 102, 241, 0.15);
        }

        .central-avatar {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            margin: 0 auto 1.5rem auto;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        }

        .card-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.75rem;
        }

        .card-desc {
            font-size: 0.95rem;
            color: #94a3b8;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }

        /* Perfectly center the Streamlit button container and style the button.
        Covers both old (class-based) and new (data-testid) Streamlit DOM structures
        so styling holds regardless of Streamlit version. */
        div.stButton,
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
            margin-top: -4.3rem;
            position: relative;
            z-index: 10;
        }

        div.stButton > button,
        div[data-testid="stButton"] > button {
            width: 65% !important;
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.7rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
            transition: all 0.2s ease !important;
            white-space: nowrap !important;
        }

        /* PRIMARY-type button: distinct resting color */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
        }

        /* PRIMARY-type button: hover must match its own color, not the generic one */
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
            transform: translateY(-1px);
        }

        /* PRIMARY-type button: active/click state must match its own color too */
        div[data-testid="stButton"] > button[kind="primary"]:active {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.6) !important;
            transform: scale(0.97) !important;
        }

        div.stButton > button:active,
        div[data-testid="stButton"] > button:active {
            transform: scale(0.97) !important;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.6) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-wrapper">
            <div class="app-badge">
                ✨ Next-Generation Academic Portal
            </div>
            <div class="main-title">Welcome to Presyra</div>
            <div class="main-subtitle">
                Select your secure workspace portal below to manage real-time tracking, compliance reports, and class rosters.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col1, col_gap, col2, _ = st.columns([1, 4.5, 0.6, 4.5, 1])

    with col1:
        st.markdown(
            """
            <div class="portal-card">
                <div class="central-avatar" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(37, 99, 235, 0.5)); border: 2px solid rgba(96, 165, 250, 0.4);">
                    👨‍🎓
                </div>
                <div class="card-title">I'm Student</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Student Portal ↗", key="btn_student", use_container_width=True, type="primary"):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="portal-card">
                <div class="central-avatar" style="background: linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(147, 51, 234, 0.5)); border: 2px solid rgba(192, 132, 252, 0.4);">
                    🧑‍🏫
                </div>
                <div class="card-title">I'm Teacher</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Teacher Portal ↗", key="btn_teacher", use_container_width=True, type="primary"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    st.markdown(
        """
        <div style="text-align: center; color: #64748b; margin-top: 5rem; font-size: 0.85rem; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 2rem;">
            &copy; 2026 Presyra Enterprise &bull; High-Performance Cloud Attendance Management
        </div>
        """,
        unsafe_allow_html=True,
    )
    footer_home()