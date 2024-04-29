import streamlit as st
from menu import menu
from app import get_user_data
from streamlit_cookies_controller import CookieController
import jwt
import os
st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")
menu(authenticated=True)
controller = CookieController()
JWT_KEY = os.getenv("JWT_KEY")

def profile_page():
    print(JWT_KEY)
    token = controller.get("auth_token") 
    print(token)
    
    if not token:
        st.error("Token nicht gefunden.")
        return
    
    try:
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        username = decoded_token.get('user_name')
        user_data = get_user_data(username)
        
        st.write("Benutzername:", user_data['username'])
        st.write("Vorname:", user_data['first_name'])
        st.write("Nachname:", user_data['last_name'])
        st.write("Geburtsdatum (JJJJ-MM-TT):", user_data['dob'])
    except jwt.ExpiredSignatureError:
        st.error("Der Token ist abgelaufen. Bitte melden Sie sich erneut an.")
    except jwt.InvalidTokenError:
        st.error("Ungültiges Token. Bitte melden Sie sich erneut an.")


if __name__ == '__main__':
    profile_page()
