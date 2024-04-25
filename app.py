import streamlit as st
from menu import menu
import pandas as pd
import os
import bcrypt

LOGIN_FILE = 'user_data.csv'

def main():
    st.title("EasyPressure")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE, 'w') as f:
            f.write("username,password_hash\n")

    choice = st.radio("Wählen Sie eine Option:", ["Anmelden", "Registeren"])
        
    if choice == "Anmelden":
        login()
    elif choice == "Registeren":
        register()

    menu(st.session_state.authenticated)
   

def register():
    st.subheader("Register")
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")
    
    if password != confirm_password:
        st.error("Passwords don't match.")
        return
    
    if st.button("Register"):
        register_new_user(username, password)
        st.success("Registration successful! Please login.")

def register_new_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with open(LOGIN_FILE, 'a') as f:
        f.write(f"{username},{hashed_password}\n")

def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            print(st.session_state.authenticated)
            st.switch_page("pages/data_entry.py")
        else:
            st.error("Invalid username or password")
            st.session_state.authenticated = False


def authenticate(username, password):
    login_df = pd.read_csv(LOGIN_FILE, header=None, names=['username', 'password_hash'])
    hashed_password = login_df[login_df['username'] == username]['password_hash'].values
    if len(hashed_password) > 0 and bcrypt.checkpw(password.encode('utf-8'), hashed_password[0].encode('utf-8')):
        return True
    else:
        return False



if __name__ == "__main__":
    main()
