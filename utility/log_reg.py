import streamlit as st

import pandas as pd
import bcrypt
import io
import base64
import os
import datetime
from github.MainClass import Github
from github import GithubException

from utility.data_repo_utilities import get_user_data
from utility.data_repo_utilities import add_user_to_github
from utility.auth_utilities import generateAuthToken
from menu import controller

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = 'user_data'
LOGIN_FILE = 'user_data.csv'
LOGIN_COLUMNS = ['username', 'password_hash', 'first_name', 'last_name', 'dob']
JWT_KEY=os.environ.get("JWT_KEY")


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

def login():
    st.title(" ")
    st.subheader(" ")
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
            