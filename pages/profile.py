import streamlit as st
st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")
from menu import menu
from utility.data_repo_utilities import get_user_data, update_user_data
import jwt
import time
from utility.auth_utilities import get_auth_token
from utility.important_variables import  REPO_NAME, LOGIN_COLUMNS, LOGIN_FILE, JWT_KEY


st.title("EasyPressure")
menu(authenticated=True)

def profile_page():
    token= get_auth_token()
    try:
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        username = decoded_token.get('user_name')
        user_data = get_user_data(username, REPO_NAME, LOGIN_FILE, LOGIN_COLUMNS)
        if user_data is not None:
            user_data = user_data.iloc[0].to_dict()
            st.write("Benutzername: " + user_data['username'])
            
            first_name = st.text_input("**Vorname:**", value=user_data['first_name'])
            last_name = st.text_input("**Nachname:**", value=user_data['last_name'])
            dob = st.text_input("**Geburtsdatum (JJJJ-MM-TT):**", value=user_data['dob'])
            
            if st.button("**Änderungen speichern**"):
                new_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'dob': dob
                }
                update_user_data(username, REPO_NAME, LOGIN_FILE, LOGIN_COLUMNS, new_data)
                st.success("Profil erfolgreich aktualisiert.")
                time.sleep(5)
                st.experimental_rerun()
        else:
            st.error("Benutzerdaten nicht gefunden.")
    except jwt.ExpiredSignatureError:
        st.error("Der Token ist abgelaufen. Bitte melden Sie sich erneut an.")
    except jwt.InvalidTokenError:
        st.error("Ungültiges Token. Bitte melden Sie sich erneut an.")
        st.switch_page('app.py')

if __name__ == '__main__':
    profile_page()
