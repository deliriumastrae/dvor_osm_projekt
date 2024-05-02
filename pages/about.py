import streamlit as st
from menu import menu
st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")
menu(authenticated=True)
st.title("EasyPressure")
st.markdown(f"You can read about our app here .")