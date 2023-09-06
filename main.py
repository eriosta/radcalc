import streamlit as st
import mre
import glenoid
import abdominal_trauma
    
def main():
    st.sidebar.title("Navigation")

    # Use radio to go to a page
    page = st.sidebar.radio("Go to", ["RADCalc", "Body", "MSK"])

    if page == "RADCalc":
        st.title("Welcome to RADCalc!")
        st.write("""
                 Hey there! Dive into RADCalc, inspired by top-tier studies from RSNA journals like Radiology and Radiographics. We've created this app with you in mind, making those often tedious radiology calculations a breeze.
                 
                 But RADCalc is more than just a calculator. It's your one-stop hub, bringing together essential references and resources. Whether you're reading cases or sharing insights in a teaching session, RADCalc ensures you're equipped with the best tools.
                 
                 Please select an option from the sidebar to proceed.
        """)

        # Adding a disclaimer
        st.subheader("Disclaimer")
        st.write("""
        RADCalc is intended for educational and informational purposes only. The results and outputs generated by this app should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider regarding any medical condition or treatment recommendations. The developers and maintainers of this application accept no responsibility for any consequences resulting directly or indirectly from the use of this application.
        """)
    
    elif page == "Body":
        choice = st.sidebar.radio("Choose the calculation", ["MR Liver Elastography (MRE)", "Grading Abdominal Trauma (2018 AAST-OIS)"])
        if choice == "MR Liver Elastography (MRE)":
            mre.run()
        elif choice == "Grading Abdominal Trauma (2018 AAST-OIS)":
            abdominal_trauma.run()

    elif page == "MSK":
        choice = st.sidebar.radio("Choose the calculation", ["Glenoid Track Assessment (Hill-Sachs Lesion)"])
        if choice == "Glenoid Track Assessment (Hill-Sachs Lesion)":
            glenoid.run()

if __name__ == "__main__":
    main()
