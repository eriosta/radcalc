import random
import string
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# Load secret JSON key for Google Sheets authentication
json_key = {
    "type": st.secrets["my_secrets"]["type"],
    "project_id": st.secrets["my_secrets"]["project_id"],
    "private_key_id": st.secrets["my_secrets"]["private_key_id"],
    "private_key": st.secrets["my_secrets"]["private_key"],
    "client_email": st.secrets["my_secrets"]["client_email"],
    "client_id": st.secrets["my_secrets"]["client_id"],
    "auth_uri": st.secrets["my_secrets"]["auth_uri"],
    "token_uri": st.secrets["my_secrets"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["my_secrets"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["my_secrets"]["client_x509_cert_url"]
}

# Function to set up the Google Sheets connection
def setup_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open("RADCalc").sheet1
    return worksheet

# Function to append data to the Google Sheet
def append_to_sheet(worksheet, name, email, message, category):
    worksheet.append_row([name, email, message, category])

def user_suggestions():
    with st.form(key='my_form'):
        st.write("Please fill out this form:")
        name = st.text_input(label='Enter your name', value='', key='name')
        email = st.text_input(label='Enter your email', value='', key='email')
        message = st.text_area(label='Enter your message', value='', key='message')
        category = st.selectbox('Select a category', ['','Error', 'New Request', 'Suggestion', 'Inquiry', 'Other'])

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            if name and email and message and category:
                # Validate email
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    correct_answer = st.session_state['num1'] + st.session_state['num2']

                else:
                    st.error("Invalid email address. Please enter a valid email.")
            else:
                st.error("All fields are required. Please fill out all fields.")

