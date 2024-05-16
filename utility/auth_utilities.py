import streamlit as st
import os
import jwt
import pandas as pd
import io
import base64
from streamlit_cookies_controller import CookieController
from github import Github, GithubException
controller = CookieController()

JWT_KEY = os.getenv("JWT_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def decode_auth_token(token):
    print(token)
    if not token:
        st.error("Token nicht gefunden.")
        
    try:
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        username = decoded_token.get('user_name')
        return username    
    except jwt.ExpiredSignatureError:
            st.error("Der Token ist abgelaufen. Bitte melden Sie sich erneut an.")
    except jwt.InvalidTokenError:
            st.error("Ungültiges Token. Bitte melden Sie sich erneut an.")

def get_user_data(username, repo_name, file_name, columns):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_user().get_repo(repo_name)
        contents = repo.get_contents(file_name)
        existing_data = pd.read_csv(io.StringIO(base64.b64decode(contents.content).decode('utf-8')), names=columns)
        user_data = existing_data[existing_data['username'] == username]
        if not user_data.empty:
            return user_data
        else:
            return None
    except GithubException as e:
        st.error(f"Fehler beim Abrufen der Benutzerdaten: {e}")
        return None

def update_user_data(username, repo_name, file_name, columns, new_data):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_user().get_repo(repo_name)
        contents = repo.get_contents(file_name)

        existing_data = pd.read_csv(io.StringIO(base64.b64decode(contents.content).decode('utf-8')), names=columns)
        
        user_index = existing_data[existing_data['username'] == username].index
        if not user_index.empty:
            for key, value in new_data.items():
                if key in columns:
                    existing_data.at[user_index[0], key] = value
        
        updated_content = existing_data.to_csv(index=False, header=False)
        repo.update_file(contents.path, "Update user data", updated_content, contents.sha)
        st.success("Benutzerdaten wurden erfolgreich aktualisiert.")
    except GithubException as e:
        st.error(f"Fehler beim Aktualisieren der Benutzerdaten: {e}")
        return None