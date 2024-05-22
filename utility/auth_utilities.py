import streamlit as st
import os
import jwt
from menu import controller

JWT_KEY = os.getenv("JWT_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

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
    token = controller.get("auth_token")
    cookie_options ={'max_age': 86400 }
    controller.set("auth_token", token, **cookie_options)
    return token