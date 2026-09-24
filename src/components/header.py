import streamlit as st


def header_home():
    st.header("Presyra")
    
def header_dashboard():
    # Create a centered container using columns
    col1, col2 = st.columns([1, 4], vertical_alignment='bottom') # Adjust ratios as needed
    with col1:
        st.image("src/components/logo.png", width=85)
    with col2:
        st.markdown("<h1 style='color:#5865F2; margin-top:10px;'>Presyra</h1>", unsafe_allow_html=True)
