import streamlit as st
from body import mre, abdominal_trauma
from msk import glenoid
from utils.suggestions import user_suggestions

def main():
    st.set_page_config(page_title='RADCalc', page_icon=':skull:')
    st.sidebar.title("RADCalc")

    # Use radio to go to a page
    page = st.sidebar.radio("Go to", ["Home", "Body", "Chest", "MSK", "Neuro", "Pediatric"])

    if page == "Home":
        st.subheader("Welcome to RADCalc!")
        st.write("""
                 Hey there! Dive into RADCalc, inspired by top-tier studies from RSNA journals like Radiology and Radiographics. We've created this app with you in mind, making those often tedious radiology calculations a breeze.
                 
                 But RADCalc is more than just a calculator. It's your one-stop hub, bringing together essential references and resources. Whether you're reading cases or sharing insights in a teaching session, RADCalc ensures you're equipped with the best tools.
                 
                 Please select an option from the sidebar to proceed.
        """)

        # Adding a disclaimer
        st.info("""
        **Disclaimer**: RADCalc is intended for educational and informational purposes only. The results and outputs generated by this app should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider regarding any medical condition or treatment recommendations. The developers and maintainers of this application accept no responsibility for any consequences resulting directly or indirectly from the use of this application.
        """)

        with st.expander("Questions, Feedback or Ideas?"):
            user_suggestions()
    
    elif page == "Body":
        st.info("Go to sidebar to start.")
        choice = st.sidebar.radio("", ["Body","MR Liver Elastography", "Grading Abdominal Trauma"])
        if choice == "MR Liver Elastography":
            mre.run()
        elif choice == "Grading Abdominal Trauma":
            abdominal_trauma.run()

    elif page == "MSK":
        st.info("Go to sidebar to start.")
        choice = st.sidebar.radio("", ["MSK","Glenoid Track Assessment"])
        if choice == "Glenoid Track Assessment":
            glenoid.run()
    
    elif page == "Chest":
        st.info("Coming Soon")

    elif page == "Neuro":
        st.info("Coming Soon")
        
    elif page == "Pediatric":
        st.info("Coming Soon")

if __name__ == "__main__":
    main()

