import streamlit as st

def authenticated_menu():
    st.sidebar.title("Menu")
    st.sidebar.page_link("pages/user.py", label="Your profile")
    st.sidebar.page_link("pages/about.py", label="About us")
    st.sidebar.button("Logout")


def unauthenticated_menu():
    st.sidebar.title("Menu")
    st.sidebar.page_link("app.py", label="Log in")

def menu(authenticated):
    if authenticated== True:
        authenticated_menu()
    elif authenticated== False:
        unauthenticated_menu()
