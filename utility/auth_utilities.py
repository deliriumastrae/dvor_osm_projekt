import streamlit as st
import jwt
from menu import controller
from utility.important_variables import JWT_KEY,controller
import streamlit.components.v1 as components

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

def get_auth_token(): 
    token = st.session_state.get('auth_token', 'No token found')
    st.session_state['auth_token'] = token
    return token