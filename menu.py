import streamlit as st
from streamlit_cookies_controller import CookieController
from PIL import Image
controller = CookieController()

def authenticated_menu():
    image = Image.open("docs/2024-05-18 13.02.22.jpeg")  

    st.sidebar.image(image, use_column_width=True)
    st.sidebar.write(" ")
    st.sidebar.page_link("pages/data_entry.py", label="**Daten eingeben 📝**", help="Geben Sie Ihre Blutdruck- und Pulswerte ein.")
    st.sidebar.write(" ")
    st.sidebar.page_link("pages/create_diagram.py", label="**Trends, Analysen & Berichte 📈**", help="Betrachten Sie Trends und erstellen Sie Berichte über Ihre Gesundheitsdaten.")
    st.sidebar.write(" ")
    st.sidebar.page_link("pages/archiv.py", label="**Archiv 🗄**", help="Sehen Sie alle gespeicherten Daten und historischen Einträge ein.")
    st.sidebar.write(" ")
    st.sidebar.page_link("pages/profile.py", label="**Profil 👤**")
    st.sidebar.write(" ")
    st.sidebar.page_link("pages/introduction.py", label="**Über EasyPressure 📘**", help="Erfahren Sie mehr über die Funktionen dieser App.")
    st.sidebar.write(" ")
    st.sidebar.page_link("pages/about.py", label="**Über uns 🥼**", help="Informationen über das Entwicklerteam und Kontaktdetails.")
    
    if st.sidebar.button('**Ausloggen 🚪**',help="Beenden Sie Ihre Sitzung sicher."):
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
