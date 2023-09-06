from captcha.image import ImageCaptcha
import random
import string
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load secret JSON key for Google Sheets authentication
json_key = st.secrets["my_secrets"]["json_key"]

# Function to set up the Google Sheets connection
def setup_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open("Your Google Sheet Name Here").sheet1
    return worksheet

# Function to append data to the Google Sheet
def append_to_sheet(worksheet, name, email, message):
    worksheet.append_row([name, email, message])

def generate_random_string(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def user_suggestions():
    st.title("CAPTCHA Display")

    # Generate CAPTCHA
    captcha_text = generate_random_string(length=5)  # Reduced length for easier CAPTCHA
    image_captcha = ImageCaptcha(width=160, height=60, fonts=None, font_sizes=(30, 40, 50))  # Adjusting font size and dimensions
    image = image_captcha.generate_image(captcha_text)
    
    with st.form(key='my_form'):
        st.write("Please fill out this form:")
        name = st.text_input(label='Enter your name')
        email = st.text_input(label='Enter your email')
        message = st.text_area(label='Enter your message')
        
        # Display CAPTCHA image on Streamlit
        st.image(image, caption="CAPTCHA", width=120)  # Reduced image display width

        captcha_input = st.text_input(label='Enter the text from the image')
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            if captcha_input.lower() == captcha_text:
                worksheet = setup_gspread()
                append_to_sheet(worksheet, name, email, message)
                st.success("Your calculator request has been sent!")
            else:
                st.error("Please verify you are a human!")
