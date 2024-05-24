import streamlit as st
from PIL import Image
from utility.important_variables import controller


def sidebar_button():
    fa_link = """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    """
    st.markdown(fa_link, unsafe_allow_html=True)

    custom_css = """
    <style>
        div.st-emotion-cache-1rgf046 button, div[data-testid="collapsedControl"] button {
            height: 60px; 
            width: 60px;
            font-size: 40px; 
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: transparent;
            border: none;
        }
        div.st-emotion-cache-1rgf046 button:before,
        div[data-testid="collapsedControl"] button:before {
            content: "\\f015";
            font-family: 'Font Awesome 5 Free';
            font-weight: 900;
            color: black;
            font-size: 40px;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

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
        st.session_state['authenticated'] = False
        st.cache_data.clear()
        try: 
            controller.remove("auth_token")
        except:
            st.error('No token to remove')
        unauthenticated_menu()
        
    sidebar_button()

def unauthenticated_menu():
    st.switch_page('app.py')

def menu(authenticated):
    if authenticated== True:
        authenticated_menu()
    elif authenticated== False:
        unauthenticated_menu()
