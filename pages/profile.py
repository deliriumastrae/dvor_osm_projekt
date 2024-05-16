import streamlit as st
from menu import menu
from utility.auth_utilities import get_user_data, update_user_data
from streamlit_cookies_controller import CookieController
import jwt
import os
controller = CookieController()

st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")
st.title("EasyPressure")
menu(authenticated=True)

JWT_KEY = os.getenv("JWT_KEY")
REPO_NAME = 'user_data'
LOGIN_FILE = 'user_data.csv'
LOGIN_COLUMNS = ['username', 'password_hash', 'first_name', 'last_name', 'dob']


def get_auth_token():
    token = controller.get("auth_token")
    cookie_options = {'max_age': 86400}
    controller.set("auth_token", token, **cookie_options)
    if not token:
        st.error("Token nicht gefunden.")
    return token

def profile_page():
    token= get_auth_token()
    try:
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        username = decoded_token.get('user_name')
        user_data = get_user_data(username, REPO_NAME, LOGIN_FILE, LOGIN_COLUMNS)
        if user_data is not None:
            user_data = user_data.iloc[0].to_dict()
            st.write("Benutzername: " + user_data['username'])
            
            first_name = st.text_input("Vorname", value=user_data['first_name'])
            last_name = st.text_input("Nachname", value=user_data['last_name'])
            dob = st.text_input("Geburtsdatum (JJJJ-MM-TT)", value=user_data['dob'])
            
            if st.button("Änderungen speichern"):
                new_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'dob': dob
                }
                update_user_data(username, REPO_NAME, LOGIN_FILE, LOGIN_COLUMNS, new_data)
                st.success("Profil erfolgreich aktualisiert.")
        else:
            st.error("Benutzerdaten nicht gefunden.")
    except jwt.ExpiredSignatureError:
        st.error("Der Token ist abgelaufen. Bitte melden Sie sich erneut an.")
    except jwt.InvalidTokenError:
        st.error("Ungültiges Token. Bitte melden Sie sich erneut an.")

if __name__ == '__main__':
    profile_page()
