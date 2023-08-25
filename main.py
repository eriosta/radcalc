import streamlit as st
import app
import test

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Choose the App", ["App", "Test"])

    if choice == "App":
        app.main_app()
    elif choice == "Test":
        test.test_app()

if __name__ == "__main__":
    main()
