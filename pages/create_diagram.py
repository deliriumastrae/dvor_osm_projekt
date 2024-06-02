import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
import jwt
from urllib.parse import quote
from datetime import datetime, timedelta
from PIL import Image as PILImage
st.set_page_config(page_title="EasyPressure", page_icon="🫀",layout="wide")
from utility.auth_utilities import decode_auth_token,get_auth_token
from menu import menu

menu(authenticated=True)
from utility.data_repo_utilities import get_user_data
from utility.important_variables import  REPO_NAME,VALUE_FILE,VALUE_FILE, VALUE_COLUMNS, LOGIN_COLUMNS, LOGIN_FILE, JWT_KEY

username = decode_auth_token(get_auth_token())

user_data = get_user_data(username, REPO_NAME, VALUE_FILE, VALUE_COLUMNS)

if user_data is not None:
    user_data_display = user_data[['date_time', 'syst_pressure', 'diast_pressure', 'pulse', 'comment']]
    user_data_display.columns = ['Datum', 'Syst/D', 'Diast/D', 'Puls', 'Kommentar']

    user_data_display['Datum'] = pd.to_datetime(user_data_display['Datum'])
    user_data_display = user_data_display.sort_values(by='Datum', ascending=True)
    user_data_display = user_data_display.fillna("")
    user_data_display['Formatted Datum'] = user_data_display['Datum'].dt.strftime('%d.%m.%Y | %H:%M')

    st.markdown("<h5 style='color: black;margin-bottom: -100px;'>Wählen Sie den Zeitraum:</h3></div>", unsafe_allow_html=True)
    period = st.selectbox("", ["Monat", "Woche", "Tag",  "Datum auswählen"])

    if period == "Monat":
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = end_date - timedelta(days=30)
    elif period == "Woche":
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = end_date - timedelta(days=7)
    elif period == "Tag":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
    else:
        start_date = st.date_input("Wähle das Startdatum", value=(datetime.now() - timedelta(days=7)))
        end_date = st.date_input("Wähle das Enddatum", value=datetime.now())
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

    filtered_data = user_data_display[(user_data_display['Datum'] >= start_date) & (user_data_display['Datum'] <= end_date)]

    if not filtered_data.empty:

        filtered_data = filtered_data.sort_values(by='Datum', ascending=False)
        filtered_data_reset = filtered_data.reset_index(drop=True)
        data_table =filtered_data_reset[['Datum', 'Syst/D', 'Diast/D', 'Puls', 'Kommentar']]
        
        fig = go.Figure()
        colors = [ 'red','#87CEEB','purple']
        for idx, col in enumerate(['Syst/D', 'Diast/D', 'Puls']):
            fig.add_trace(go.Scatter(
            x=filtered_data['Datum'], 
            y=filtered_data[col], 
            mode='lines+markers', 
            name=col, 
            line=dict(color=colors[idx])  
            ))

            fig.update_layout(
                title='Diagramm',
                title_font_size=20,
                xaxis=dict(
                    title='Datum',
                    titlefont=dict(size=16,color='black'),
                ),
                
                yaxis=dict(
                    title='Blutdruck/Puls',
                    titlefont=dict(size=16,color='black'),
                    nticks=20 
                ),

                font=dict(size=18),
                legend=dict(font=dict(size=14), orientation="h", y=-0.3),
                margin=dict(l=40, r=40, t=80, b=40),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hoverlabel=dict(font=dict(size=14))
            )


        st.plotly_chart(fig,use_container_width=True)

        current_date = datetime.now().strftime("%d-%m-%Y %H:%M")
        chart_path = f"{current_date}.png"

else:
    st.write("Keine Benutzerdaten sind vorhanden.")

st.markdown("""<b>
<span style='font-size: 18px; color: #a2272c;'>Bitte beachten Sie: Diese Daten dienen nur zu Informationszwecken und sollten nicht für Selbst-Diagnosen oder Behandlungen verwendet werden. Es wird empfohlen, jegliche Auffälligkeiten oder Bedenken mit Ihrem Arzt zu besprechen. Ihr Gesundheitszustand sollte regelmäßig von einem Fachmann überwacht werden.</span></b>
""", unsafe_allow_html=True)

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image

if st.button('**WEITER ZUM SPEICHERN**', help='Speichern Sie das Diagramm als PDF zur manuellen Bildexportierung'):
    try:
        save_directory = 'path_to_save'
        pdf_file_name = f"{current_date}.pdf"

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
    
        pdf_file_path = os.path.join(save_directory, pdf_file_name)

        
        doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        elements = []

        fig.update_layout(yaxis=dict(title='',nticks=20, tickfont=dict(size=9)),xaxis=dict(tickfont=dict(size=10)))
        fig.write_image(chart_path, format='png', width=800, height=400)  
        img = PILImage.open(chart_path)
        img_rotated = img.rotate(270, expand=True)
        img_rotated.save(chart_path)
        image = Image(chart_path, width=456, height=636)  
        elements.append(image)


        table_data = [data_table.columns.tolist()] + data_table.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)

        
        
        doc.build(elements)
    
        st.success(f'**↓ PDF-Datei speichern**')
        with open(pdf_file_path, "rb") as file:
            btn = st.download_button(
            label="**PDF herunterladen**",
            data=file,
            file_name=pdf_file_name,
            mime='application/pdf')

    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

token = get_auth_token()
        
try:
    decoded_token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    username = decoded_token.get('user_name')
    user_data =  get_user_data(username,REPO_NAME, LOGIN_FILE, LOGIN_COLUMNS)
    user_data= user_data.iloc[0].to_dict()
except jwt.ExpiredSignatureError:
        st.error("Der Token ist abgelaufen. Bitte melden Sie sich erneut an.")
        
Ihr_Name= (user_data['first_name'] + " " + user_data['last_name'])

try: 
    subject = f"Übermittlung meiner Blutdruckdaten vom {current_date}." + Ihr_Name

    body = (f"Sehr geehrte(r) Herr/Frau Doktor/in\n\n"
            "anbei sende ich Ihnen meine Blutdruckdaten. "
            "Ich bitte Sie, diese zu überprüfen und mich über eventuelle Auffälligkeiten oder Anpassungen meiner Behandlung zu informieren.\n\n"
            "Vielen Dank für Ihre Unterstützung und Betreuung.\n\n"
            "Freundlichen Grüsse\n"
            + Ihr_Name )    

    encoded_subject = quote(subject)
    encoded_body = quote(body)

    doctor_email = st.text_input("**GEBEN SIE DIE E-MAIL-ADRESSE IHRES ARZTES EIN**",help="Geben Sie die gültige E-Mail-Adresse Ihres Arztes ein, an die Sie Ihre Blutdruckdaten senden möchten. Bestätigen Sie die Eingabe mit Enter.")

    mailto_link = f"mailto:{doctor_email}?subject={encoded_subject}&body={encoded_body}"
    st.markdown(f"<a href='{mailto_link}' target='_blank' style='color: #a2272c; text-transform: uppercase;'>**Daten per E-Mail senden**</a>", unsafe_allow_html=True,help='Bestätigen Sie die Eingabe mit Enter!')
    st.info('Nach der Eingabe drücken Sie bitte die Enter-Taste, um die Eingabe zu bestätigen.')
except: 
    st.error ("Bitte tragen Sie Ihre aktuellen Blutdruck- und Pulswerte ein.")