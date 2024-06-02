import streamlit as st
import jwt
from utility.important_variables import JWT_KEY

def generateAuthToken(username):
    if username:
        payload = {
            "user_name": username
        }
        token = jwt.encode(payload, JWT_KEY, algorithm='HS256')
        return token 
    else:
        return None

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
            st.switch_page('app.py')

def get_auth_token(): 
    token = st.session_state.get('auth_token', 'No token found') 
    return token