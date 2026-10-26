import streamlit as st
from landing_page import show_landing_page

st.set_page_config(
    page_title="MediVision AI",
    page_icon="🏥",
    layout="wide"
)

if "entered" not in st.session_state:
    st.session_state["entered"] = False

if not st.session_state["entered"]:
    show_landing_page()
else:
    st.success("Welcome to MediVision AI!")
    st.header("Medical Analysis Dashboard")

    if st.button("Back to Welcome Page"):
        st.session_state["entered"] = False
        st.rerun()