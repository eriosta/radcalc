import streamlit as st

def determine_grade():
    grade = None

    laceration = st.radio("Laceration", ["Less than 1 cm", "1-3 cm", "Greater than 3 cm"], key="laceration")
    subscap_hematoma = st.radio("Subscapular hematoma", ["Less than 10% surface area", "10-50%", "Greater than 50%"], key="subscap_hematoma")
    intraparenchymal_hematoma = st.radio("Intraparenchymal hematoma", ["Less than 5 cm", "Greater than or equal to 5 cm"], key="intraparenchymal_hematoma")
    devascularization = st.radio("Devascularization", ["25-75%", "None of these"], key="devascularization")
    vascular_injury = st.radio("AVF, pseudoaneurysm, vascular injury", ["Present", "Absent"], key="vascular_injury")
    active_bleeding = st.radio("Active bleeding", ["Confined active parenchymal active bleeding", "Active bleeding extending to peritoneum", "None of these"], key="active_bleeding")
    shattered_spleen = st.radio("Shattered spleen", ["Present", "Absent"], key="shattered_spleen")

    # Check for Grade V criteria first
    if active_bleeding == "Active bleeding extending to peritoneum" and shattered_spleen == "Present":
        grade = "V"
    # Then, check for Grade IV
    elif devascularization == "25-75%" and vascular_injury == "Present" and active_bleeding == "Confined active parenchymal active bleeding":
        grade = "IV"
    # Then Grade III
    elif laceration == "Greater than 3 cm" and subscap_hematoma == "Greater than 50%" and intraparenchymal_hematoma == "Greater than or equal to 5 cm":
        grade = "III"
    # Then Grade II
    elif laceration == "1-3 cm" and subscap_hematoma == "10-50%" and intraparenchymal_hematoma == "Less than 5 cm":
        grade = "II"
    # Finally, Grade I
    elif laceration == "Less than 1 cm" and subscap_hematoma == "Less than 10% surface area":
        grade = "I"

    return grade

st.title("Spleen Grading System")
grade = determine_grade()
if grade:
    st.write(f"The spleen's grade is: Grade {grade}")
else:
    st.write("No matching grade found according to the inputs provided.")
