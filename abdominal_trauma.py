import streamlit as st

def determine_grade():
    grade = None

    laceration = st.radio("Laceration", ["<1 cm", "1-3 cm", "greater than 3 cm"], key="laceration")
    subscap_hematoma = st.radio("Subscapular hematoma", ["<10% surface area", "10-50%", "greater than 50%"], key="subscap_hematoma")
    intraparenchymal_hematoma = st.radio("Intraparenchymal hematoma", ["<5 cm", "greater than or equal to 5 cm"], key="intraparenchymal_hematoma")
    devascularization = st.radio("Devascularization", ["25-75%", "None of these"], key="devascularization")
    vascular_injury = st.radio("AVF, pseudoaneurysm, vascular injury", ["Present", "Absent"], key="vascular_injury")
    active_bleeding = st.radio("Active bleeding", ["Confined active parenchymal active bleeding", "active bleeding extending to peritoneum", "None of these"], key="active_bleeding")
    shattered_spleen = st.radio("Shattered spleen", ["Present", "Absent"], key="shattered_spleen")

    if laceration == "<1 cm" and subscap_hematoma == "<10% surface area":
        grade = "I"
    elif laceration == "1-3 cm" and subscap_hematoma == "10-50%" and intraparenchymal_hematoma == "<5 cm":
        grade = "II"
    elif laceration == "greater than 3 cm" and subscap_hematoma == "greater than 50%" and intraparenchymal_hematoma == "greater than or equal to 5 cm":
        grade = "III"
    elif devascularization == "25-75%" or vascular_injury == "Present" or active_bleeding == "Confined active parenchymal active bleeding":
        grade = "IV"
    elif active_bleeding == "active bleeding extending to peritoneum" or shattered_spleen == "Present":
        grade = "V"

    return grade

st.title("Spleen Grading System")
grade = determine_grade()
if grade:
    st.write(f"The spleen's grade is: Grade {grade}")
else:
    st.write("No matching grade found according to the inputs provided.")
