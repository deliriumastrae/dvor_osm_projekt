import streamlit as st
import base64
import os
from os.path import join, dirname
from dotenv import load_dotenv

st.set_page_config(page_title="EasyPressure", page_icon="🫀")
from utility.log_reg import login, register
from utility.auth_utilities import get_auth_token
from menu import sidebar_button, controller 

dotenv_path=join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = 'user_data'
LOGIN_FILE = 'user_data.csv'
LOGIN_COLUMNS = ['username', 'password_hash', 'first_name', 'last_name', 'dob']
JWT_KEY=os.environ.get("JWT_KEY")

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def main():
    image_path = 'docs/anmelden.jpeg' 
    encoded_image = get_image_base64(image_path)  

    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        
        </style>
        """, unsafe_allow_html=True)


    st.sidebar.title("Menü")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "token" not in st.session_state:
        token = get_auth_token()
        if token:
            st.session_state.token = token

    page = st.sidebar.radio("**Wählen Sie eine Option:**", ["**EINLOGEN**", "**REGISTRIEREN**"])

    if page == "**EINLOGEN**":
        login()
    elif page == "**REGISTRIEREN**":
        register()
    sidebar_button()

if __name__ == "__main__":
    main()