import random
import string
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize session state
st.session_state['num1'] = st.session_state.get('num1', random.randint(1, 10))
st.session_state['num2'] = st.session_state.get('num2', random.randint(1, 10))

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

def generate_random_string(length=5):
    letters = string.digits  # Use all lowercase letters and digits
    return ''.join(random.choice(letters) for i in range(length))

def user_suggestions():
    with st.form(key='my_form'):
        st.write("Please fill out this form:")
        name = st.text_input(label='Enter your name', value='', key='name')
        email = st.text_input(label='Enter your email', value='', key='email')
        message = st.text_area(label='Enter your message', value='', key='message')
        category = st.selectbox('Select a category', ['','Error', 'New Request', 'Suggestion', 'Inquiry', 'Other'])
        st.write(f"Please solve this simple math problem to verify you're not a bot: {st.session_state['num1']} + {st.session_state['num2']}")
        user_answer = st.number_input(label='Your answer to the math problem:', step=1, format="%d")
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            correct_answer = st.session_state['num1'] + st.session_state['num2']
            if int(user_answer) == correct_answer:
                worksheet = setup_gspread()
                append_to_sheet(worksheet, name, email, message, category)
                st.success("Your message has been sent!")
                # Reset the numbers so that new ones will be generated for the next time
                st.session_state['num1'] = random.randint(1, 10)
                st.session_state['num2'] = random.randint(1, 10)
            else:
                st.error(f"Incorrect! The correct answer is {correct_answer}. Please verify you are a human!")