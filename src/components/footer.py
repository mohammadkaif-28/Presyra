import streamlit as st

def footer_home():
    st.markdown("""
                <div style="margin-top: 2rem; display: flex; gap: 6px; justify-content: center;item-align: center;">
                <p style="font-weight:bold; color:white;"> Created by Mohammad Kaif </p>
                </div>
                """,unsafe_allow_html=True)
    
def footer_dashboard():
    st.space()
    st.space()
    st.space()
    st.divider()
    st.markdown("""
                <div style="margin-top: 2rem; display: flex; gap: 6px; justify-content: center;item-align: center;">
                <p style="font-weight:bold; color:#000047;"> Created by Mohammad Kaif </p>
                </div>
                """,unsafe_allow_html=True)