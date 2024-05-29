import streamlit as st
st.set_page_config(page_title="EasyPressure", page_icon="🫀",layout="wide")
from menu import menu
from datetime import datetime
import time
from utility.auth_utilities import decode_auth_token,get_auth_token
from utility.data_repo_utilities import add_data_to_github
menu(authenticated=True)

username= decode_auth_token(get_auth_token())
st.markdown(f"**Willkommen bei EasyPressure, {username}!** Bitte tragen Sie Ihre aktuellen Blutdruck- und Pulswerte ein.")

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