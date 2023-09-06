from captcha.image import ImageCaptcha
import random
import string
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
def append_to_sheet(worksheet, name, email, message):
    worksheet.append_row([name, email, message])

def generate_random_string(length=5):
    letters = string.digits  # Use all lowercase letters and digits
    return ''.join(random.choice(letters) for i in range(length))

def user_suggestions():
    length_captcha = 4
    width = 300  # Increase the width
    height = 200  # Increase the height

    # Generate CAPTCHA
    captcha_text = generate_random_string(length=length_captcha).lower()  # No need to lower() here as all letters are already lowercase
    image_captcha = ImageCaptcha(width=width, height=height, fonts=None, font_sizes=(40, 50))  # Increase the font size
    image = image_captcha.generate_image(captcha_text)
    
    with st.form(key='my_form'):
        st.write("Please fill out this form:")
        name = st.text_input(label='Enter your name')
        email = st.text_input(label='Enter your email')
        message = st.text_area(label='Enter your message')
        
        # Display CAPTCHA image on Streamlit
        # st.image(image, caption="CAPTCHA",use_column_width=True)  # Reduced image display width

        captcha_input = st.text_input(label='Enter the text from the image')
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            # if captcha_input.lower() == captcha_text:
            worksheet = setup_gspread()
            append_to_sheet(worksheet, name, email, message)
            st.success("Your calculator request has been sent!")
            # else:
            #     st.error("Please verify you are a human!")

