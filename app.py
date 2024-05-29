import streamlit as st
st.set_page_config(page_title="EasyPressure", page_icon="🫀")

from os.path import join, dirname
from dotenv import load_dotenv

from utility.log_reg import login, register
from menu import sidebar_button

dotenv_path=join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def main():
    st.sidebar.title("Menü")
    page = st.sidebar.radio("**Wählen Sie eine Option:**", ["**EINLOGGEN**", "**REGISTRIEREN**"])

    if "authenticated" not in st.session_state:
        st.session_state['authenticated'] = False

    if page == "**EINLOGGEN**":
        login()
    elif page == "**REGISTRIEREN**":
        register()

    
    sidebar_button()

if __name__ == "__main__":
    main()