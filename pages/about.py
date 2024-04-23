import streamlit as st
from menu import menu

menu(authenticated=True)

st.title("About us")
st.markdown(f"You can read about our app here .")