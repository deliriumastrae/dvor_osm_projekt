import os
import io
import base64
from github import Github
import pandas as pd
import streamlit as st
from menu import menu
from datetime import datetime
import time
from utility.auth_utilities import decode_auth_token
from streamlit_cookies_controller import CookieController
controller = CookieController()
st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")
menu(authenticated=True)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = 'user_data'
VALUE_FILE = 'user_value.csv'
COLUMNS = ['username', 'syst_pressure', 'diast_pressure', 'pulse', 'comment', 'date_time']
JWT_KEY = os.environ.get("JWT_KEY")

@st.cache_data
def get_auth_token():
    token = controller.get("auth_token")
    return token

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
username= decode_auth_token(get_auth_token())
st.write("Benutzername:", username)

st.markdown("<h2 style='color: black; font-weight: bold; font-size: 18px; margin-bottom: -80px;'>Bitte wählen Sie den Eingabetyp:</h2>", unsafe_allow_html=True)
option = st.radio("", ("Schieberegler", "Zahleneingabe"))

st.markdown("<div style='text-align: center;'><h3 style='color: black;margin-bottom: -50px;'>Systolischer Druck</h3></div>", unsafe_allow_html=True)
if option == "Schieberegler":
    syst_pressure = st.slider(" ", min_value=0, max_value=300, value=120, format="%d", help="Geben Sie Ihren Systolischen Druck ein.")
else:
    syst_pressure = st.number_input(" ", value=120, format="%d", key="syst_pressure", help="Geben Sie Ihren Systolischen Druck ein.")

st.markdown("<div style='text-align: center;'><h3 style='color: black;margin-bottom: -50px;'>Diastolischer Druck</h3></div>", unsafe_allow_html=True)
if option == "Schieberegler":
    diast_pressure = st.slider(" ", min_value=0, max_value=200, value=80, format="%d", help="Geben Sie Ihren Diastolischen Druck ein.")
else:
    diast_pressure = st.number_input(" ", value=80, format="%d", key="diast_pressure", help="Geben Sie Ihren Diastolischen Druck ein.")

st.markdown("<div style='text-align: center;'><h3 style='color: black;margin-bottom: -50px;'>Puls</h3></div>", unsafe_allow_html=True)
if option == "Schieberegler":
    pulse = st.slider(" ", min_value=0, max_value=200, value=60, help="Geben Sie Ihren Puls ein.")
else:
    pulse = st.number_input(" ", value=60, key="pulse", help="Geben Sie Ihr Puls ein.")

st.markdown("<div style='text-align: center;'><h3 style='color: black;margin-bottom: -50px;'>Kommentar</h3></div>", unsafe_allow_html=True)
comment = st.text_area("")

now = datetime.now()
current_date = now.date()
current_time = now.time()

current_time_rounded = current_time.replace(second=0, microsecond=0)

st.markdown("<h3 style='color: black;margin-bottom: -50px;'>Datum</h3></div>", unsafe_allow_html=True)
user_date = st.date_input("", value=current_date)

st.markdown("<h3 style='color: black;margin-bottom: -50px;'>Zeit</h3></div>", unsafe_allow_html=True)
user_time = st.time_input("", value=current_time_rounded)

user_time_rounded = user_time.replace(second=0, microsecond=0)

date_time = datetime.combine(user_date, user_time_rounded)

if st.button("Daten speichern", type="primary",help="Hier klicken, um die Daten zu speichern"):
    if add_data_to_github(username, syst_pressure, diast_pressure, pulse, comment, date_time):
        with st.empty():
            st.success("Daten erfolgreich gespeichert!")
            time.sleep(5)
            st.empty()
    else:
        st.error("Fehler beim Speichern der Daten.")