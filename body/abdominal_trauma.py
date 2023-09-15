import streamlit as st
    
def spleen_grading():
    def determine_grade():
        grade = None

        laceration = st.radio("Laceration", ["Less than 1 cm", "1-3 cm", "Greater than 3 cm"], key="laceration")
        subscap_hematoma = st.radio("Subscapular hematoma", ["Less than 10% surface area", "10-50%", "Greater than 50%"], key="subscap_hematoma")
        intraparenchymal_hematoma = st.radio("Intraparenchymal hematoma", ["Less than 5 cm", "Greater than or equal to 5 cm"], key="intraparenchymal_hematoma")
        devascularization = st.radio("Devascularization", ["25-75%", "None"], key="devascularization")
        vascular_injury = st.radio("AVF, pseudoaneurysm, vascular injury", ["Present", "Absent"], key="vascular_injury")
        active_bleeding = st.radio("Active bleeding", ["Confined active parenchymal active bleeding", "Active bleeding extending to peritoneum", "None of these"], key="active_bleeding")
        shattered_spleen = st.radio("Shattered spleen", ["Absent", "Present"], key="shattered_spleen")

        # Check for Grade V criteria first
        if active_bleeding == "Active bleeding extending to peritoneum" or shattered_spleen == "Present":
            grade = "V"
        # Then, check for Grade IV
        elif devascularization == "25-75%" or vascular_injury == "Present" or active_bleeding == "Confined active parenchymal active bleeding":
            grade = "IV"
        # Then Grade III
        elif laceration == "Greater than 3 cm" or subscap_hematoma == "Greater than 50%" or intraparenchymal_hematoma == "Greater than or equal to 5 cm":
            grade = "III"
        # Then Grade II
        elif laceration == "1-3 cm" or subscap_hematoma == "10-50%" or intraparenchymal_hematoma == "Less than 5 cm":
            grade = "II"
        # Finally, Grade I
        elif laceration == "Less than 1 cm" or subscap_hematoma == "Less than 10% surface area":
            grade = "I"

        return grade

    st.title("Spleen Grading System")
    grade = determine_grade()
    if grade:
        st.info(f"The spleen's grade is: Grade {grade}")
        if grade == "V":
            with st.expander("Grade V Criteria"):
                st.markdown("* Active bleeding extending to peritoneum")
                st.markdown("* Shattered spleen is Present")
        elif grade == "IV":
            with st.expander("Grade IV Criteria"):
                st.markdown("* Devascularization is 25-75%")
                st.markdown("* Vascular injury is Present")
                st.markdown("* Active bleeding is Confined active parenchymal active bleeding")
        elif grade == "III":
            with st.expander("Grade III Criteria"):
                st.markdown("* Laceration is Greater than 3 cm")
                st.markdown("* Subscapular hematoma is Greater than 50%")
                st.markdown("* Intraparenchymal hematoma is Greater than or equal to 5 cm")
        elif grade == "II":
            with st.expander("Grade II Criteria"):
                st.markdown("* Laceration is 1-3 cm")
                st.markdown("* Subscapular hematoma is 10-50%")
                st.markdown("* Intraparenchymal hematoma is Less than 5 cm")
        elif grade == "I":
            with st.expander("Grade I Criteria"):
                st.markdown("* Laceration is Less than 1 cm")
                st.markdown("* Subscapular hematoma is Less than 10% surface area")
    else:
        st.error("No matching grade found according to the inputs provided.")

def liver_grading():
    def determine_liver_grade():
        grade = None

        lac = st.radio("Laceration", ["Less than 1 cm", "1-3 cm", "Greater than 3 cm"], key="lac")
        subscap_hematoma = st.radio("Subscapular hematoma", ["Less than 10% surface area", "10-50%", "Greater than 50%","Ruptured"], key="subscap_hematoma_liver")
        intraparenchymal_hemorrhage = st.radio("Intraparenchymal hemorrhage", ["Less than 10 cm", "Greater than 10 cm","Ruptured"], key="intraparenchymal_hemorrhage")
        lobar_parenchymal_disruption = st.radio("Lobar parenchymal disruption", ["None","25-75%", "Greater than 75%"], key="lobar_parenchymal_disruption")
        active_bleeding = st.radio("Active bleeding", ["Confined to liver", "Extending to peritoneum"], key="active_bleeding_liver")
        venous_injury = st.radio("Venous injury (IVC/major hepatic veins)", ["Absent", "Present"], key="venous_injury")

        # Grade V
        if lobar_parenchymal_disruption == "Greater than 75%" or venous_injury == "Present":
            grade = "V"
        # Grade IV
        elif lobar_parenchymal_disruption == "25-75%" or active_bleeding == "Extending to peritoneum":
            grade = "IV"
        # Grade III
        elif intraparenchymal_hemorrhage == "Greater than 10 cm" or intraparenchymal_hemorrhage == "Ruptured" or subscap_hematoma == "Greater than 50%" or subscap_hematoma == "Ruptured" or lac =="Greater than 3 cm" or active_bleeding == "Confined to liver":
            grade = "III"
        # Grade II
        elif lac == "1-3 cm" or subscap_hematoma == "10-50%" or intraparenchymal_hemorrhage == "Less than 10 cm":
            grade = "II"
        # Grade I
        elif lac == "Less than 1 cm" or subscap_hematoma == "Less than 10% surface area":
            grade = "I"
        
        return grade

    st.title("Liver Grading System")
    grade = determine_liver_grade()
    if grade:
        st.info(f"The liver's grade is: Grade {grade}")
        if grade == "V":
            with st.expander("Grade V Criteria"):
                st.markdown("* Lobar parenchymal disruption is Greater than 75%")
                st.markdown("* Venous injury (IVC/major hepatic veins) is Present")
        elif grade == "IV":
            with st.expander("Grade IV Criteria"):
                st.markdown("* Lobar parenchymal disruption is 25-75%")
                st.markdown("* Active bleeding is Extending to peritoneum")
        elif grade == "III":
            with st.expander("Grade III Criteria"):
                st.markdown("* Intraparenchymal hemorrhage is Greater than 10 cm")
                st.markdown("* Subscapular hematoma is Greater than 50%")
                st.markdown("* Laceration is Greater than 3 cm")
                st.markdown("* Active bleeding is Confined to liver")
        elif grade == "II":
            with st.expander("Grade II Criteria"):
                st.markdown("* Laceration is 1-3 cm")
                st.markdown("* Subscapular hematoma is 10-50%")
                st.markdown("* Intraparenchymal hemorrhage is Less than 10 cm")
        elif grade == "I":
            with st.expander("Grade I Criteria"):
                st.markdown("* Laceration is Less than 1 cm")
                st.markdown("* Subscapular hematoma is Less than 10% surface area")
    else:
        st.error("No matching grade found according to the inputs provided.")

def kidney_grading():
    st.title("Kidney Grading System")
    st.write("Kidney grading system coming soon...")

def run():
    # Sidebar navigation
    selection = st.sidebar.radio("Abdominal Trauma Grading:", ["Home", "Spleen", "Liver", "Kidneys"])

    if selection == "Home":
        st.title("Abdominal Trauma Grading")
        st.write("Select an organ from the sidebar to proceed.")
    elif selection == "Spleen":
        spleen_grading()
    elif selection == "Liver":
        liver_grading()
    elif selection == "Kidneys":
        kidney_grading()
