import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from utility.auth_utilities import decode_auth_token
from utility.auth_utilities import get_user_data
from streamlit_cookies_controller import CookieController
from menu import menu
from datetime import datetime, timedelta
import plotly.io as pio

@st.cache_data
def get_auth_token():
    token = controller.get("auth_token")
    return token

# Настройка страницы
st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")
menu(authenticated=True)
controller = CookieController()
username = decode_auth_token(controller.get("auth_token"))
st.write("Benutzername:", username)

# Загрузите ваш API ключ из переменных окружения
sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
from_email = os.getenv('FROM_EMAIL')  # Ваш отправной email

# Получение и обработка данных
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = 'user_data'
VALUE_FILE = 'user_value.csv'
VALUE_COLUMNS = ['username', 'syst_pressure', 'diast_pressure', 'pulse', 'comment', 'date_time']

# Функция для получения диапазона дат
def get_date_range(period):
    if period == "Tag":
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    elif period == "Woche":
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = end_date - timedelta(days=end_date.weekday() + 1) if end_date.weekday() != 6 else end_date - timedelta(days=6)
    elif period == "Monat":
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = datetime(end_date.year, end_date.month, 1)
    else:
        start_date = st.date_input("Wähle das Startdatum", value=(datetime.now() - timedelta(days=7)))
        end_date = st.date_input("Wähle das Enddatum", value=datetime.now())
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    return start_date, end_date

# Функция для обработки пользовательских данных
def process_user_data(user_data):
    user_data_display = user_data[['date_time', 'syst_pressure', 'diast_pressure', 'pulse', 'comment']]
    user_data_display.columns = ['Datum', 'Systolischer Druck', 'Diastolischer Druck', 'Puls', 'Kommentar']
    user_data_display['Datum'] = pd.to_datetime(user_data_display['Datum'])
    user_data_display = user_data_display.sort_values(by='Datum', ascending=True)
    user_data_display = user_data_display.fillna("")
    user_data_display['Formatted Datum'] = user_data_display['Datum'].dt.strftime('%d.%m.%Y | %H:%M')

    st.markdown("<h5 style='color: black;margin-bottom: -100px;'>Wählen Sie den Zeitraum:</h5>", unsafe_allow_html=True)
    period = st.selectbox("", ("Tag", "Woche", "Monat", "Datum auswählen"))
    start_date, end_date = get_date_range(period)
    filtered_data = user_data_display[(user_data_display['Datum'] >= start_date) & (user_data_display['Datum'] <= end_date)]

    if not filtered_data.empty:
        display_chart(filtered_data)
    else:
        st.write("Keine Benutzerdaten verfügbar.")

# Функция для отображения графика
def display_chart(filtered_data):
    fig = go.Figure()
    for col in ['Systolischer Druck', 'Diastolischer Druck', 'Puls']:
        fig.add_trace(go.Scatter(x=filtered_data['Datum'], y=filtered_data[col], mode='lines', name=col))
    fig.update_layout(
        title='Diagramm',
        title_font_size=30,
        xaxis=dict(title='Datum', titlefont=dict(size=30, color='black')),
        yaxis=dict(title='Blutdruck/Puls', titlefont=dict(size=30, color='black')),
        font=dict(size=40),
        legend=dict(font=dict(size=18)),
        margin=dict(l=40, r=40, t=80, b=40),
        plot_bgcolor='white',
        paper_bgcolor='white',
        hoverlabel=dict(font=dict(size=16)),
        width=1000,
        height=700
    )
    st.plotly_chart(fig)
    chart_path = "pressure_chart.pdf"
    pio.write_image(fig, chart_path, format='pdf')
    recipient_email = st.text_input("Enter recipient email:")
    if st.button('Send Email with Chart'):
        send_email_with_attachment(from_email, recipient_email, 'Daily Pressure Report', 'Here is your daily pressure report attached.', chart_path)

user_data = get_user_data(username, REPO_NAME, VALUE_FILE, VALUE_COLUMNS)
if user_data is not None:
    process_user_data(user_data)
else:
    st.write("Keine Benutzerdaten verfügbar.")

# Функция для отправки писем
def send_email_with_attachment(from_email, to_email, subject, content, file_path):
    sg = SendGridAPIClient(sendgrid_api_key)
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    with open(file_path, 'rb') as f:
        data = f.read()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('pressure_chart.pdf'),
        FileType('application/pdf'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    try:
        response = sg.send(message)
        st.success('Email sent successfully!')
    except Exception as e:
        st.error(f'An error occurred: {e}')
