import streamlit as st
from streamlit_cookies_controller import CookieController
controller = CookieController()

def authenticated_menu():
    st.sidebar.title("Menü")
    st.sidebar.page_link("pages/profile.py", label="Profil")
    st.sidebar.page_link("pages/data_entry.py", label="Werte eingeben")
    st.sidebar.page_link("pages/create_diagram.py", label="Diagramm")
    st.sidebar.page_link("pages/archiv.py", label="Archiv")
    st.sidebar.page_link("pages/introduction.py", label="Einführung")
    st.sidebar.page_link("pages/about.py", label="Über uns")
    if st.sidebar.button('Abmelden'):
        st.session_state.authenticated = False
        st.cache_data.clear()
        if controller.get("auth_token"):
            controller.remove("auth_token")
        else:
            st.warning("The session token has already been deleted or does not exist.")
        st.switch_page('app.py')

def unauthenticated_menu():
    st.sidebar.title("Menu")
    st.sidebar.page_link("app.py", label="Log in")

def menu(authenticated):
    if authenticated== True:
        authenticated_menu()
    elif authenticated== False:
        unauthenticated_menu()
