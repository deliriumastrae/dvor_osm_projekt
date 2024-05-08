import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
import time
import jwt
from urllib.parse import quote
from utility.auth_utilities import decode_auth_token
from streamlit_cookies_controller import CookieController
from menu import menu
from datetime import datetime, timedelta

st.set_page_config(page_title="EasyPressure", page_icon="🫀",layout="wide")

menu(authenticated=True)
controller = CookieController()
from utility.auth_utilities import get_user_data

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = 'user_data'
VALUE_FILE = 'user_value.csv'
VALUE_COLUMNS = ['username', 'syst_pressure', 'diast_pressure', 'pulse', 'comment', 'date_time']

JWT_KEY = os.getenv("JWT_KEY")
LOGIN_FILE = 'user_data.csv'
LOGIN_COLUMNS = ['username', 'password_hash', 'first_name', 'last_name', 'dob']

def get_auth_token():
    token = controller.get("auth_token")
    cookie_options = {'max_age': 86400}
    controller.set("auth_token", token, **cookie_options)
    return token

username = decode_auth_token(get_auth_token())

user_data = get_user_data(username, REPO_NAME, VALUE_FILE, VALUE_COLUMNS)

if user_data is not None:
    user_data_display = user_data[['date_time', 'syst_pressure', 'diast_pressure', 'pulse', 'comment']]
    user_data_display.columns = ['Datum', 'Systolischer Druck', 'Diastolischer Druck', 'Puls', 'Kommentar']

    user_data_display['Datum'] = pd.to_datetime(user_data_display['Datum'])
    user_data_display = user_data_display.sort_values(by='Datum', ascending=True)
    user_data_display = user_data_display.fillna("")
    user_data_display['Formatted Datum'] = user_data_display['Datum'].dt.strftime('%d.%m.%Y | %H:%M')

    st.markdown("<h5 style='color: black;margin-bottom: -100px;'>Wählen Sie den Zeitraum:</h3></div>", unsafe_allow_html=True)
    period = st.selectbox("", ["Tag", "Woche", "Monat", "Datum auswählen"])

    if period == "Tag":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
    elif period == "Woche":
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = end_date - timedelta(days=7)
    elif period == "Monat":
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = end_date - timedelta(days=30)
    else:
        start_date = st.date_input("Wähle das Startdatum", value=(datetime.now() - timedelta(days=7)))
        end_date = st.date_input("Wähle das Enddatum", value=datetime.now())
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

    filtered_data = user_data_display[(user_data_display['Datum'] >= start_date) & (user_data_display['Datum'] <= end_date)]

    if not filtered_data.empty:
        fig = go.Figure()
        colors = [ 'red','#87CEEB','purple']
        for idx, col in enumerate(['Systolischer Druck', 'Diastolischer Druck', 'Puls']):
            fig.add_trace(go.Scatter(
            x=filtered_data['Datum'], 
            y=filtered_data[col], 
            mode='lines', 
            name=col, 
            line=dict(color=colors[idx])  
            ))

            fig.update_layout(
                title='Diagramm',
                title_font_size=20,
                xaxis=dict(
                    title='Datum',
                    titlefont=dict(
                        size=16,
                        color='black'
                    ),
                ),
                yaxis=dict(
                    title='Blutdruck/Puls',
                    titlefont=dict(
                        size=16,
                        color='black'
                    ),
                ),
                font=dict(size=18),
                legend=dict(font=dict(size=14), orientation="h", y=-0.3),
                margin=dict(l=40, r=40, t=80, b=40),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hoverlabel=dict(font=dict(size=14))
            )


    #     custom_css = """
    # <style>
    # .modebar-btn, .modebar-btn:active {
    #     width: 10px !important;  
    #     height: 40px !important;
    # }
    # .modebar-btn svg {
    #     width: 40px !important; 
    #     height: 30px !important; 
    # }
    # </style>
    # """
    #     st.markdown(custom_css, unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "toImageButtonOptions": {"format": "png"}})

        current_date = datetime.now().strftime("%d-%m-%Y %H:%M")
        chart_path = f"{current_date}.png"



        # if st.button('Diagramm speichern', help='Lokale Schpeicherung Ihres Diagramms'):
        #     fig.write_image(chart_path,format='png', width=1600, height=1200)
        #     with open(chart_path, "rb") as file:
        #         btn = st.download_button(
        #         label="Diagramm herunterladen",
        #         data=file,
        #         file_name=f"{current_date}.png",
        #         mime="image/png")
        #     st.write("Saving chart to:", chart_path)
            
        #     st.success('Diagramm erfolgreich gespeichert!')
        #     time.sleep(5)



    if st.button('Weiter zum Speichern', help='Speichern Sie das Diagramm als PDF zur manuellen Bildexportierung'):
        try:
            
            save_directory = 'path_to_save'
            pdf_file_name = f"{current_date}.pdf"

            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            pdf_file_path = os.path.join(save_directory, pdf_file_name)

            fig.write_image(pdf_file_path)
            st.success('↓ Speichern Sie Ihr Diagramm als PDF.')
            with open(pdf_file_path, "rb") as file:
                btn = st.download_button(
                    label="Diagramm herunterladen",
                    data=file,
                    file_name=pdf_file_name,
                    mime='application/pdf')
            
            

        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

    token = get_auth_token()
    cookie_options ={'max_age': 86400 }
    controller.set("auth_token", token, **cookie_options)
    if not token:
        st.error("Token nicht gefunden.")
        
    try:
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        username = decoded_token.get('user_name')
        user_data =  get_user_data(username,REPO_NAME, LOGIN_FILE, LOGIN_COLUMNS)
        user_data= user_data.iloc[0].to_dict()
    except jwt.ExpiredSignatureError:
        st.error("Der Token ist abgelaufen. Bitte melden Sie sich erneut an.")
        
    Ihr_Name= (user_data['first_name'] + " " + user_data['last_name'])

    subject = f"Übermittlung meiner Blutdruckdaten vom {current_date}." + Ihr_Name
    body = (f"Sehr geehrte(r) Herr/Frau Doktor/in\n\n"
            "anbei sende ich Ihnen meine Blutdruckdaten. "
            "Ich bitte Sie, diese zu überprüfen und mich über eventuelle Auffälligkeiten oder Anpassungen meiner Behandlung zu informieren.\n\n"
            "Vielen Dank für Ihre Unterstützung und Betreuung.\n\n"
            "Freundlichen Grüsse\n"
            + Ihr_Name )    

    encoded_subject = quote(subject)
    encoded_body = quote(body)

    doctor_email = st.text_input("Geben Sie die E-Mail-Adresse Ihres Arztes ein")

    mailto_link = f"mailto:{doctor_email}?subject={encoded_subject}&body={encoded_body}"
    st.markdown(f"<a href='{mailto_link}' target='_blank'>Daten per E-Mail senden</a>", unsafe_allow_html=True)
    
else:
    st.write("Keine Benutzerdaten verfügbar.")