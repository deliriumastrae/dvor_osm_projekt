import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import bcrypt
import io
import base64
from jose import jwt
import os
import datetime
from github.MainClass import Github
from github import GithubException
from os.path import join, dirname
from dotenv import load_dotenv

st.set_page_config(page_title="EasyPressure", page_icon="🫀")
controller = CookieController()
from utility.auth_utilities import get_user_data

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
        token = controller.get("auth_token")
        if token:
            st.session_state.token = token

    page = st.sidebar.radio("**Wählen Sie eine Option:**", ["**EINLOGEN**", "**REGISTRIEREN**"])

    if page == "**EINLOGEN**":
        login()
    elif page == "**REGISTRIEREN**":
        register()

def register():
    st.title(" ")
    st.title("Registeren") 
    username = st.text_input("**BENUTZERNAME:**", key="register_username")
    password = st.text_input("**PASSWORT:**", type="password", key="register_password")
    confirm_password = st.text_input("**PASSWORT BESTÄTIGEN:**", type="password", key="register_confirm_password")
    first_name = st.text_input("**VORNAME:**", key="register_first_name")
    last_name = st.text_input("**NACHNAME:**", key="register_last_name")

    dob = st.date_input("**GEBURTSDATUM (JJJJ-MM-TT)**", min_value=datetime.date(1930, 1, 1), max_value=datetime.date(2024, 12, 31), key="register_dob")

    if not username or not password or not confirm_password or not first_name or not last_name or not dob:
        st.warning("**Bitte füllen Sie alle Felder aus und und drücken Sie Enter.**")
        return
    
    if password != confirm_password:
        st.error("Die Passwörter stimmen nicht überein.")
        return
    
    if st.button("Registrieren"):
        if add_user_to_github(username, password, first_name, last_name, dob):
            st.success("Registrierung erfolgreich! Bitte einloggen.")
        else:
            st.error("Fehler beim Registrieren.")
            
def add_user_to_github(username, password, first_name, last_name, dob):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_user().get_repo(REPO_NAME)
        
        contents = repo.get_contents(LOGIN_FILE)
        existing_data = pd.read_csv(io.StringIO(base64.b64decode(contents.content).decode('utf-8')), names=LOGIN_COLUMNS)
        
        if username in existing_data['username'].values:
            st.error("Benutzername existiert bereits.")
            return False
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_data = pd.DataFrame({'username': [username], 'password_hash': [hashed_password], 
                                 'first_name': [first_name], 'last_name': [last_name], 'dob': [dob]})
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_content = updated_data.to_csv(index=False, header=False)
        repo.update_file(contents.path, "Neuen Benutzer hinzufügen", updated_content, contents.sha)
        
        return True
    except GithubException as e:
        st.error(f"Fehler beim Hinzufügen des Benutzers zu GitHub: {e}")
        return False

def login():
    try:
        controller = CookieController()
    except Exception as e:
        st.error(f"Error initializing cookie controller: {str(e)}")
    st.title(" ")
    st.title("Einlogen")
    
    username = st.text_input("**BENUTZERNAME:**", key="login_username")
    password = st.text_input("**PASSWORT:**", type="password", key="login_password")
    
    
    if st.button("Anmelden"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            user_data = get_user_data(username, REPO_NAME, LOGIN_FILE, LOGIN_COLUMNS)
            username = user_data['username'].item()
            token = generateAuthToken(username)
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            cookie_options = {
            'max_age': 86400, 
            'expires': expires,  
            'path': '/'  
            }
            if token:
                st.session_state.token = token
                controller.set("auth_token", token, **cookie_options)
            st.switch_page("pages/data_entry.py")
        else:
            st.error("Ungültiger Benutzername oder Passwort")
            st.session_state.authenticated = False


def generateAuthToken(username):
    if username:
        payload = {
            "user_name": username
        }
        token = jwt.encode(payload, JWT_KEY, algorithm='HS256')
        return token 
    else:
        return None
    
def authenticate(username, password):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_user().get_repo(REPO_NAME)
        contents = repo.get_contents(LOGIN_FILE)
        existing_data = pd.read_csv(io.StringIO(base64.b64decode(contents.content).decode('utf-8')), names=LOGIN_COLUMNS)
        st.session_state.username = username
        if username not in existing_data['username'].values:
            return False
        hashed_password = existing_data.loc[existing_data['username'] == username, 'password_hash'].iloc[0]
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
   
        
    except GithubException as e:
        st.error(f"Fehler bei der Benutzerauthentifizierung: {e}")
        return False

if __name__ == "__main__":
    main()