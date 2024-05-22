import os
from streamlit_cookies_controller import CookieController

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
JWT_KEY = os.environ.get("JWT_KEY")

REPO_NAME = 'user_data'

VALUE_FILE = 'user_value.csv'
VALUE_COLUMNS = ['username', 'syst_pressure', 'diast_pressure', 'pulse', 'comment', 'date_time']

LOGIN_FILE = 'user_data.csv'
LOGIN_COLUMNS = ['username', 'password_hash', 'first_name', 'last_name', 'dob']

controller = CookieController()