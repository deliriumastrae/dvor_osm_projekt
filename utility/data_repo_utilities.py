import streamlit as st

import pandas as pd
import bcrypt
import io
import base64
import os
from github.MainClass import Github
from github import GithubException
import base64
from github import Github
import pandas as pd

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = 'user_data'
LOGIN_FILE = 'user_data.csv'
LOGIN_COLUMNS = ['username', 'password_hash', 'first_name', 'last_name', 'dob']
JWT_KEY=os.environ.get("JWT_KEY")

VALUE_FILE = 'user_value.csv'
COLUMNS = ['username', 'syst_pressure', 'diast_pressure', 'pulse', 'comment', 'date_time']

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
    
def add_data_to_github(username, syst_pressure, diast_pressure, pulse, comment, date_time):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_user().get_repo(REPO_NAME)
        
        try:
            contents = repo.get_contents(VALUE_FILE)
            existing_data = pd.read_csv(io.StringIO(base64.b64decode(contents.content).decode('utf-8')), names=COLUMNS)
        except Exception as e:
            st.warning(f"Fehler beim Laden der Datei: {e}")
            existing_data = pd.DataFrame(columns=COLUMNS)
        
        new_data = pd.DataFrame({'username': [username], 'syst_pressure': [syst_pressure],
                                 'diast_pressure': [diast_pressure], 'pulse': [pulse], 'comment': [comment], 'date_time': [date_time]})
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_content = updated_data.to_csv(index=False, header=False)

        repo.update_file(VALUE_FILE, "Neue Benutzerdaten hinzufügen", updated_content, contents.sha)
        
        return True
    except Exception as e:
        st.error(f"Fehler beim Hinzufügen von Daten zu GitHub: {e}")
        return False
    