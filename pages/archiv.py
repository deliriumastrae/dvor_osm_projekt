import streamlit as st
from menu import menu
from streamlit_cookies_controller import CookieController
import os
import pandas as pd
from utility.auth_utilities import decode_auth_token
from utility.auth_utilities import get_user_data

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = 'user_data'
VALUE_FILE = 'user_value.csv'
VALUE_COLUMNS = ['username','syst_pressure','diast_pressure','pulse','comment','date_time']

st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")

menu(authenticated=True)

controller = CookieController()

@st.cache_data
def get_auth_token():
    token = controller.get("auth_token")
    return token

username = decode_auth_token(get_auth_token())

user_data = get_user_data(username, REPO_NAME, VALUE_FILE, VALUE_COLUMNS)

st.title("EasyPressure")
st.write("Benutzername:", username)
if user_data is not None:

    user_data_display = user_data[['date_time', 'syst_pressure', 'diast_pressure', 'pulse', 'comment']]
    user_data_display.columns = ['Datum', 'Systolischer Druck', 'Diastolischer Druck', 'Puls', 'Kommentar']

    user_data_display['Datum'] = pd.to_datetime(user_data_display['Datum'])

    user_data_display = user_data_display.sort_values(by='Datum', ascending=False)
    
    user_data_display = user_data_display.fillna("")
    
    user_data_display['Datum'] = user_data_display['Datum'].dt.strftime('%d.%m.%Y') + " | " + user_data_display['Datum'].dt.strftime('%H:%M')
    
    html_table = "<table style='font-size:16px;'><tr><th>Datum</th><th>Systolischer Druck</th><th>Diastolischer Druck</th><th>Puls</th><th>Kommentar</th></tr>"
    for index, row in user_data_display.iterrows():
        html_table += "<tr>"
        for value in row:
            html_table += "<td>" + str(value) + "</td>"
        html_table += "</tr>"
    html_table += "</table>"
    st.write(html_table, unsafe_allow_html=True)
else:
    st.write("Benutzerdaten sind nicht gefunden.")


st.session_state.user_data_display = user_data_display
st.cache(user_data_display)
