import streamlit as st
from menu import menu
st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")
menu(authenticated=True)

st.title("This page is available to all users")
st.markdown(f"hallo.")