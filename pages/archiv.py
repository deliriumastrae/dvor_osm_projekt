import streamlit as st
from menu import menu 
import pandas as pd
import time
from utility.auth_utilities import decode_auth_token, get_auth_token
from utility.data_repo_utilities import get_user_data, update_value_data
from utility.important_variables import REPO_NAME,VALUE_FILE,VALUE_COLUMNS
st.set_page_config(page_title="EasyPressure", page_icon="🫀",layout="wide")

menu(authenticated=True)

username = decode_auth_token(get_auth_token())

user_data = get_user_data(username, REPO_NAME, VALUE_FILE, VALUE_COLUMNS)

st.write('**Sie können Ihre Eingaben der letzten 2 Tage bearbeiten:**')
user_data_test = user_data.copy()

user_data_test['date_time'] = pd.to_datetime(user_data_test['date_time'])
    
user_data_test = user_data_test.sort_values(by='date_time', ascending=False)

unique_dates = user_data_test['date_time'].dt.date.unique()
sorted_dates = sorted(unique_dates, reverse=True)

if len(sorted_dates) >= 2:
    date1, date2 = sorted_dates[:2]
else:
    date1 = sorted_dates[0]
    date2 = None

filtered_data1 = user_data_test[user_data_test['date_time'].dt.date == date1].copy()
if date2:
    filtered_data2 = user_data_test[user_data_test['date_time'].dt.date == date2].copy()
    filtered_data = pd.concat([filtered_data1, filtered_data2])
else:
    filtered_data = filtered_data1

updated_rows = []

for index, row in filtered_data.iterrows():
        unique_key = f"{index}_{row['date_time'].strftime('%Y%m%d_%H%M%S')}"
        datetime_str = row['date_time'].strftime('%d.%m | %H:%M')
        with st.expander(f"**ZEIT: {datetime_str}**"):
            syst_pressure = st.number_input(
                f"Systolischer Druck ({datetime_str})", 
                value=int(row['syst_pressure']), 
                step=1, 
                key=f"syst_{unique_key}"
            )
            diast_pressure = st.number_input(
                f"Diastolischer Druck ({datetime_str})", 
                value=int(row['diast_pressure']), 
                step=1, 
                key=f"diast_{unique_key}"
            )
            pulse = st.number_input(
                f"Puls ({datetime_str})", 
                value=int(row['pulse']), 
                step=1, 
                key=f"pulse_{unique_key}"
            )
            comment = st.text_input(
                f"Kommentar ({datetime_str})", 
                value=row['comment'], 
                key=f"comment_{unique_key}"
            )

            updated_row = {
                'username': username,
                'syst_pressure': syst_pressure,
                'diast_pressure': diast_pressure,
                'pulse': pulse,
                'comment': comment,
                'date_time': row['date_time']
            }
            updated_rows.append(updated_row)

if st.button(f"**Änderungen speichern**"):

        for updated_row in updated_rows:
            update_value_data(username, REPO_NAME, VALUE_FILE, VALUE_COLUMNS, updated_row)
        st.success(f"Daten erfolgreich aktualisiert.")
        time.sleep(1.5)
        st.experimental_rerun()
        

###
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

try:
    st.session_state.user_data_display = user_data_display
except: 
    st.error ("Bitte tragen Sie Ihre aktuellen Blutdruck- und Pulswerte ein.")
