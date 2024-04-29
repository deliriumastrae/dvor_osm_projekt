import streamlit as st

def authenticated_menu():
    st.sidebar.title("Menu")
    st.sidebar.page_link("pages/profile.py", label="Profil")
    st.sidebar.page_link("pages/data_entry.py", label="Werte eingeben")
    st.sidebar.page_link("pages/create_diagram.py", label="Diagramm")
    st.sidebar.page_link("pages/send_the_data.py", label="Daten versenden")
    st.sidebar.page_link("pages/archiv.py", label="Archiv")
    st.sidebar.page_link("pages/introduction.py", label="Einführung")
    st.sidebar.page_link("pages/about.py", label="Über uns/Fragen/Feedback")
    if st.sidebar.button('Abmelden'):
        st.session_state.authenticated = False
        print(st.session_state.authenticated)
        st.switch_page('app.py')

def unauthenticated_menu():
    st.sidebar.title("Menu")
    st.sidebar.page_link("app.py", label="Log in")

def menu(authenticated):
    if authenticated== True:
        authenticated_menu()
    elif authenticated== False:
        unauthenticated_menu()
